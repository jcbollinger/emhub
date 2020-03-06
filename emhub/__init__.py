# **************************************************************************
# *
# * Authors:     J.M. De la Rosa Trevin (delarosatrevin@scilifelab.se) [1]
# *              Grigory Sharov (gsharov@mrc-lmb.cam.ac.uk) [2]
# *
# * [1] SciLifeLab, Stockholm University
# * [2] MRC Laboratory of Molecular Biology (MRC-LMB)
# *
# * This program is free software; you can redistribute it and/or modify
# * it under the terms of the GNU General Public License as published by
# * the Free Software Foundation; either version 3 of the License, or
# * (at your option) any later version.
# *
# * This program is distributed in the hope that it will be useful,
# * but WITHOUT ANY WARRANTY; without even the implied warranty of
# * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# * GNU General Public License for more details.
# *
# * You should have received a copy of the GNU General Public License
# * along with this program; if not, write to the Free Software
# * Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA
# * 02111-1307  USA
# *
# *  All comments concerning this program package may be sent to the
# *  e-mail address 'delarosatrevin@scilifelab.se'
# *
# **************************************************************************

import os
import json
from glob import glob

from flask import Flask, render_template, request, make_response

from . import utils
from .api import send_json_data, api_bp


here = os.path.abspath(os.path.dirname(__file__))
templates = [os.path.basename(f) for f in glob(os.path.join(here, 'templates', '*.html'))]


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.register_blueprint(api_bp, url_prefix='/api')

    app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
    app.config.from_mapping(SECRET_KEY='dev')
    dbPath = os.path.join(app.instance_path, 'emhub.sqlite')

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/index')
    def index():
        # get status!=Finished sessions only
        sessions = app.sm.get_sessions(condition='status!="Finished"')
        running_sessions = []
        for session in sessions:
            # we need to pass scope name for the link name and the session id
            running_sessions.append({
                'microscope': session.microscope,
                'id': session.id})

        return render_template('main.html', sessions=running_sessions)

    @app.route('/get_mic_thumb', methods=['POST'])
    def get_mic_thumb():
        micId = int(request.form['micId'])
        sessionId = int(request.form['sessionId'])
        session = app.sm.load_session(sessionId)
        setObj = session.data.get_sets()[0]
        mic = session.data.get_item(setObj['id'], micId,
                                    dataAttrs=['micThumbData',
                                               'psdData',
                                               'shiftPlotData'])

        return send_json_data(mic._asdict())

    @app.route('/get_content', methods=['POST'])
    def get_content():
        # content = session-live-id#id
        content = request.form['content_id']
        content_id = content.split('-id')[0]
        session_id = content.split('-id')[-1] or None
        content_template = content_id + '.html'

        if content_template in templates:
            return render_template(content_template,
                                   **ContentData.get(content_id, session_id))

        return "<h1>Template '%s' not found</h1>" % content_template


    @app.template_filter('basename')
    def basename(filename):
        """Convert a string to all caps."""
        return os.path.basename(filename)

    class ContentData:
        # To have a quick way to retrieve data based on the content-id, we just
        # need to call the function get_$content-id_data and it will be
        # automatically retrieved. In the name, we need to replace the - in
        # the content id by _
        @classmethod
        def get(cls, content_id, session_id):
            get_func_name = 'get_%s' % content_id.replace('-', '_')
            get_func = getattr(cls, get_func_name, None)
            return {} if get_func is None else get_func(session_id)

        @classmethod
        def get_sessions_overview(cls, session_id=None):
            sessions = app.sm.get_sessions(condition='status!="Finished"',
                                           orderBy='microscope')
            return {'sessions': sessions}

        @classmethod
        def get_session_live(cls, session_id):
            session = app.sm.load_session(session_id)
            firstSetId = session.data.get_sets()[0]['id']
            mics = session.data.get_items(firstSetId, ['location', 'ctfDefocus'])
            defocusList = [m.ctfDefocus for m in mics]
            sample = ['Defocus'] + defocusList

            bar1 = {'label': 'CTF Defocus',
                    'data': defocusList}

            return {'sample': sample,
                    'bar1': bar1,
                    'micrographs': mics,
                    'session': session}

        @classmethod
        def get_sessions_stats(cls, session_id=None):
            sessions = app.sm.get_sessions()
            return {'sessions': sessions}

    app.jinja_env.filters['reverse'] = basename
    from emhub.session.sqlalchemy import SessionManager
    app.sm = SessionManager(dbPath)

    @app.teardown_appcontext
    def shutdown_session(exception=None):
        app.sm.close()

    return app
