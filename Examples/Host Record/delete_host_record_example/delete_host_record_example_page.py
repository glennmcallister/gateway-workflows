# Copyright 2017 BlueCat Networks. All rights reserved.

# Various Flask framework items.
import os
import sys

from flask import url_for, redirect, render_template, flash, g, request

from bluecat import route, util
import config.default_config as config
from main_app import app
from .delete_host_record_example_form import GenericFormTemplate


def module_path():
    encoding = sys.getfilesystemencoding()
    return os.path.dirname(os.path.abspath(unicode(__file__, encoding)))

# The workflow name must be the first part of any endpoints defined in this file.
# If you break this rule, you will trip up on other people's endpoint names and
# chaos will ensue.
@route(app, '/delete_host_record_example/delete_host_record_example_endpoint')
@util.workflow_permission_required('delete_host_record_example_page')
@util.exception_catcher
def delete_host_record_example_delete_host_record_example_page():
    form = GenericFormTemplate()
    # Remove this line if your workflow does not need to select a configuration
    form.configuration.choices = util.get_configurations(default_val=True)
    return render_template('delete_host_record_example_page.html',
                           form=form,
                           text=util.get_text(module_path(), config.language),
                           options=g.user.get_options())


@route(app, '/delete_host_record_example/form', methods=['POST'])
@util.workflow_permission_required('delete_host_record_example_page')
@util.exception_catcher
def delete_host_record_example_delete_host_record_example_page_form():
    form = GenericFormTemplate()
    # Remove this line if your workflow does not need to select a configuration
    form.configuration.choices = util.get_configurations(default_val=True)
    if form.validate_on_submit():
        try:
            # Retrieve form attributes
            configuration = g.user.get_api().get_entity_by_id(form.configuration.data)

            view = configuration.get_view(request.form['view'])

            # Retrieve host record
            host_record = view.get_host_record(request.form['host_record'] + '.' + request.form['parent_zone'])

            # Retrieve host record attributes for flash message
            host_record_name = host_record.get_property('absoluteName')
            host_record_id = util.safe_str(host_record.get_id())

            # Delete host record
            host_record.delete()

            # Put form processing code here
            g.user.logger.info('Success - Host  (A) Record ' + host_record_name + ' Deleted with Object ID: ' +
                               host_record_id)
            flash('Success - Host  (A) Record ' + host_record_name + ' Deleted with Object ID: ' +
                  host_record_id, 'succeed')
            return redirect(url_for('delete_host_record_exampledelete_host_record_example_delete_host_record_example_page'))
        except Exception as e:
            flash(util.safe_str(e))
            # Log error and render workflow page
            g.user.logger.warning('%s' % util.safe_str(e), msg_type=g.user.logger.EXCEPTION)
            return render_template('delete_host_record_example_page.html',
                                   form=form,
                                   text=util.get_text(module_path(), config.language),
                                   options=g.user.get_options())
    else:
        g.user.logger.info('Form data was not valid.')
        return render_template('delete_host_record_example_page.html',
                               form=form,
                               text=util.get_text(module_path(), config.language),
                               options=g.user.get_options())
