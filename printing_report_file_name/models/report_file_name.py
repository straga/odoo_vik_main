# -*- coding: utf-8 -*-
import pdb
from openerp.addons.web.http import Controller, route, request
from openerp.addons.report.controllers.main import ReportController
from openerp.addons.web.controllers.main import _serialize_exception, content_disposition
from openerp.osv import osv
from openerp import http
import simplejson
import time
import logging
from werkzeug import exceptions, url_decode
from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse
from werkzeug.datastructures import Headers
import openerp.tools as tools
import openerp.addons.decimal_precision as dp

import re

_logger = logging.getLogger(__name__)

class NewReportController(ReportController):
    @route(['/report/download'], type='http', auth="user")
    def report_download(self, data, token):
        """This function is used by 'qwebactionmanager.js' in order to trigger the download of
        a pdf/controller report.

        :param data: a javascript array JSON.stringified containg report internal url ([0]) and
        type [1]
        :returns: Response with a filetoken cookie and an attachment header
        """
        requestcontent = simplejson.loads(data)
        url, type = requestcontent[0], requestcontent[1]
        try:
            if type == 'qweb-pdf':
                reportname = url.split('/report/pdf/')[1].split('?')[0]
		
                docids = None
                if '/' in reportname:
                    reportname, docids = reportname.split('/')

                    if docids:
                        # Generic report:
                        response = self.report_routes(reportname, docids=docids, converter='pdf')
                        #switch reportname with the evaluated attachment attribute of the action if available
                        docids = [int(i) for i in docids.split(',')]
                        report_obj = request.registry['report']
                        cr, uid, context = request.cr, request.uid, request.context
                        report = report_obj._get_report_from_name(cr, uid, reportname)

                        report_ename = "%s_" % (report.name)
                        obj = report_obj.pool[report.model].browse(cr, uid, docids[0])


                        if len(docids) > 1: # if more than one reports for printing
                            prefex = "(time.strftime('%d/%m/%Y')) + ('.pdf')"
                        else:


                            prefex_name = ""
                            try:
                                if obj.name:
                                    prefex_name = "(object.name)+'_'"
                            except:
                                pass

                            prefex_state = ""
                            try:
                                if obj.state:
                                    prefex_state = "'_'+(object.state)+'_'"
                            except:
                                pass

                            prefex = prefex_name + prefex_state + " + (time.strftime('%d/%m/%Y')) + ('.pdf')"

                        #_logger.warning("prefex : %s", prefex  )


                        try:
                            reportname = eval(prefex, {'object': obj, 'time': time}).split('.pdf')[0]
                        except:
                            pass
                            reportname = report_ename

                        reportname = report_ename+reportname

			    # Remove all non-word characters (everything except numbers and letters)
     			reportname = re.sub(r"[^\w\s]", '', reportname)

     			# Replace all runs of whitespace with a single dash
     			reportname = re.sub(r"\s+", '-', reportname)
			    #_logger.warning("reportname-1 : %s", reportname  )


                else:
                    # Particular report:
                    data = url_decode(url.split('?')[1]).items()  # decoding the args represented in JSON
                    response = self.report_routes(reportname, converter='pdf', **dict(data))


		        #_logger.warning("reportname-2 : %s", reportname  )
                response.headers.add('Content-Disposition', 'attachment; filename=%s.pdf;' % reportname)
                response.set_cookie('fileToken', token)
                return response


            elif type =='controller':
                reqheaders = Headers(request.httprequest.headers)
                response = Client(request.httprequest.app, BaseResponse).get(url, headers=reqheaders, follow_redirects=True)
                response.set_cookie('fileToken', token)
                return response
            else:
                return
        except Exception, e:
            se = _serialize_exception(e)
            error = {
                'code': 200,
                'message': "Odoo Server Error",
                'data': se
            }
            return request.make_response(html_escape(simplejson.dumps(error)))