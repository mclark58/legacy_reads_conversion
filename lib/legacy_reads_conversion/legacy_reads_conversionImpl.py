#i -*- coding: utf-8 -*-
#BEGIN_HEADER
import sys
import traceback
from biokbase.workspace.client import Workspace as workspaceService
import requests
requests.packages.urllib3.disable_warnings()
import subprocess
import os
import re
from pprint import pprint, pformat
import uuid
from ReadsUtils.ReadsUtilsClient import ReadsUtils as ReadsUtils
#END_HEADER


class legacy_reads_conversion:
    '''
    Module Name:
    legacy_reads_conversion

    Module Description:
    Utilities for converting KBaseAssembly types to KBaseFile types
    '''

    ######## WARNING FOR GEVENT USERS #######
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    #########################################
    VERSION = "0.0.1"
    GIT_URL = ""
    GIT_COMMIT_HASH = ""
    
    #BEGIN_CLASS_HEADER

    def _upload_reads (self,refid, callbackURL, input_params):
      ref = [refid] 
      DownloadReadsParams={'read_libraries':ref}
      dfUtil = ReadsUtils(callbackURL)
      x=dfUtil.download_reads(DownloadReadsParams)
 
      uploadReadParams = {}
      fwd_file    =  x['files'][ref[0]]['files']['fwd']
      otype =  x['files'][ref[0]]['files']['otype']
      #case of interleaved
      if (otype == 'interleaved'):
            uploadReadParams = {'fwd_file': fwd_file, 
                                'wsname': input_params['workspace_name'],
                                'name': input_params['output'],
                                'rev_file':'',
                                'sequencing_tech': input_params['sequencing_tech'],
                                'single_genome': input_params['single_genome'],
                                'interleaved': 1
                                }

        #case of separate pair 
      if (otype == 'paired'):
            rev_file    =  x['files'][ref[0]]['files']['rev']
            uploadReadParams = {'fwd_file': fwd_file, 
                                'wsname': input_params['workspace_name'],
                                'name': input_params['output'],
                                'rev_file':rev_file,
                                'sequencing_tech': input_params['sequencing_tech'],
                                'single_genome': input_params['single_genome']
                                }

        #case of single end 
      if (otype == 'single'):
            uploadReadParams = {'fwd_file': fwd_file, 
                                'wsname': input_params['workspace_name'],
                                'name': input_params['output'],
                                'rev_file':'',
                                'sequencing_tech': input_params['sequencing_tech'],
                                'single_genome': input_params['single_genome']
                                }
      y = dfUtil.upload_reads(uploadReadParams)
      return y['obj_ref']
 
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        self.shockURL = config['shock-url']
        self.scratch = os.path.abspath(config['scratch'])
        self.handleURL = config['handle-service-url']

        self.callbackURL = os.environ.get('SDK_CALLBACK_URL')
        if self.callbackURL == None:
            raise ValueError ("SDK_CALLBACK_URL not set in environment")

        if not os.path.exists(self.scratch):
            os.makedirs(self.scratch)
	#os.chdir(self.scratch)
        #END_CONSTRUCTOR
        pass
    

    def run_legacy_reads_conversion(self, ctx, input_params):
        """
        :param input_params: instance of type "legacyReadsConversionParams"
           (This module has methods to convert legacy KBaseAssembly types to
           KBaseFile types. 1. KBaseAssembly.SingleEndLibrary to
           KBaseFile.SingleEndLibrary 2. KBaseAssembly.PairedEndLibrary to
           KBaseFile.PairedEndLibrary workspace_name    - the name of the
           workspace for input/output read_library_name - the name of the
           KBaseAssembly.SingleEndLibrary or KBaseAssembly.PairedEndLibrary)
           -> structure: parameter "workspace_name" of String, parameter
           "read_library_name" of String
        :returns: instance of type "ConversionReport" -> structure: parameter
           "report_name" of String, parameter "report_ref" of String
        """
        # ctx is the context object
        # return variables are: report
        #BEGIN run_legacy_reads_conversion
        
        # Download reads files
        token = ctx['token']
        wsClient = workspaceService(self.workspaceURL, token=token)
        headers = {'Authorization': 'OAuth '+token}

        info=None
        readLibrary=None
        try:
            readLibrary = wsClient.get_objects([{'name': input_params['read_library_name'],
                                                 'workspace' : input_params['workspace_name']}])[0]
            info = readLibrary['info']
            readLibrary = readLibrary['data']
        except Exception as e:
            raise ValueError('Unable to get read library object from workspace: (' + str(input_params['workspace_name'])+ '/' + str(input_params['read_library_name']) +')' + str(e))
 #       pp = pprint.PrettyPrinter(indent=4)   
#        ref=['11665/5/2', '11665/10/7', '11665/11/1' ]
        #ref=['11665/10/7']
        callbackURL = self.callbackURL
        input_reads_ref = str(input_params['workspace_name']) + '/' + str(input_params['read_library_name'])
        output_reads_ref = self._upload_reads (input_reads_ref, callbackURL, input_params)
        #self._upload_reads (ref[0], callbackURL, input_params)
        #self._upload_reads (ref[1], callbackURL, input_params)
        #self._upload_reads (ref[2], callbackURL, input_params)
        provenance = [{}]
        if 'provenance' in ctx:
            provenance = ctx['provenance']
        # add additional info to provenance here, in this case the input data object reference
        provenance[0]['input_ws_objects']=[input_reads_ref]
     
        report = ''
        report += 'Successfully converted'
        
        reportObj = {
            'objects_created':[],
            'text_message':report
        }
        reportObj['objects_created'].append({'ref': output_reads_ref, 'description': 'Converted reads'})

        reportName = 'run_legacy_reads_conversion_'+str(hex(uuid.getnode()))
        report_info = wsClient.save_objects({
            'workspace':input_params['workspace_name'],
            'objects':[
                 {
                  'type':'KBaseReport.Report',
                  'data':reportObj,
                  'name':reportName,
                  'meta':{},
                  'hidden':1, # important!  make sure the report is hidden
                  'provenance':provenance
                 }
            ] })[0]  
        print('saved Report: '+pformat(report_info))

        report = { "report_name" : reportName,"report_ref" : str(report_info[6]) + '/' + str(report_info[0]) + '/' + str(report_info[4]) }

 
        #exporter = ReadsUtils.download_reads(self.cfg)
        #result = exporter.export(ctx, params)
        #pp.pprint (x)
        #Check type of read
        # Get statistics from reads files

        # Upload files back to shock in proper way

        # Create report type


        #END run_legacy_reads_conversion

        # At some point might do deeper type checking...
        if not isinstance(report, dict):
            raise ValueError('Method run_legacy_reads_conversion return value ' +
                             'report is not type dict as required.')
        # return the results
        return [report]

    def status(self, ctx):
        #BEGIN_STATUS
        returnVal = {'state': "OK", 'message': "", 'version': self.VERSION, 
                     'git_url': self.GIT_URL, 'git_commit_hash': self.GIT_COMMIT_HASH}
        #END_STATUS
        return [returnVal]
