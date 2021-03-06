#!/usr/bin/env python
#------------------------------------------------------------------------------
# Copyright 2014 Esri
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#==============================================================================
#Name:          CreateBatchFileToRunCreateServiceList.py
#
#Purpose:       Creates a batch file containing the syntax to execute the CreateServiceList.py
#               for each portal user in the specified portal.
#
#==============================================================================
import sys
import os

append_to_sys_path = os.path.join(os.path.join((os.path.dirname(os.path.dirname(sys.argv[0]))), 'Publish'), 'Portal')
sys.path.append(append_to_sys_path)

#import portalpy
import json
from portalpy import Portal

script_name = sys.argv[0]
script_path = os.path.dirname(sys.argv[0])
exitErrCode = 1
username_exclude = ['system_publisher']

def main():
    
    totalSuccess = True
    out_file = None
    
    # Check arguments
    results = check_args()
    if not results:
        sys.exit(exitErrCode)
    
    # Get parameter values
    portal_url, user, password, output_file, access_mode = results
    
    try:
       
        # Create portal object
        portal = Portal(portal_url, user, password)
        
        if not portal:
            raise Exception('ERROR: Could not create "portal" object.')
        
        if not portal.logged_in_user():
            raise Exception('\nERROR: Could not sign in with specified credentials.')
        
        # Get portal users
        portal_users = portal.org_users()
        
        out_file = open(output_file, access_mode)
        out_file_dir = os.path.dirname(output_file)
    
        for portal_user in portal_users:
            user_name = portal_user['username']
            if user_name not in username_exclude:
                service_list_outfile = os.path.join(out_file_dir, '{}_servicelist.txt'.format(user_name))
                service_list_qc_outfile = os.path.join(out_file_dir, '{}_qc_servicelist.txt'.format(user_name))
                script_parameters = '{} {} {} {} {} {} {} > {}'.format(os.path.join(script_path, 'CreateServiceList.py'),
                        portal_url, user, password, service_list_outfile, 'OVERWRITE', user_name, service_list_qc_outfile)
                out_file.write(script_parameters + '\n')
        
        print '\nDone. Output written to: {}\n'.format(output_file)
        
    except:
        totalSuccess = False
        
        # Get the traceback object
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
     
        # Concatenate information together concerning the error into a message string
        pymsg = "PYTHON ERRORS:\nTraceback info:\n" + tbinfo + "\nError Info:\n" + str(sys.exc_info()[1])
     
        # Print Python error messages for use in Python / Python Window
        print
        print "***** ERROR ENCOUNTERED *****"
        print pymsg + "\n"
        
    finally:
        if hasattr(out_file, 'close'):
            out_file.close()
        if totalSuccess:
            sys.exit(0)
        else:
            sys.exit(1)

def check_args():
    # ---------------------------------------------------------------------
    # Check arguments
    # ---------------------------------------------------------------------

    if len(sys.argv) < 5:
        
        print '\n' + script_name + ' <PortalURL> <AdminUser> <AdminUserPassword> <OutputFile> {OVERWRITE|APPEND}'

        print '\nWhere:'
        print '\n\t{:<20}: {}'.format('<PortalURL>', 'URL of Portal (i.e. https://fully_qualified_domain_name/arcgis).')
        print '\n\t{:<20}: {}'.format('<AdminUser>', 'Portal admin user.')
        print '\n\t{:<20}: {}'.format('<AdminUserPassword>', 'Password for portal admin user.')
        print '\n\t{:<20}: {}'.format('<OutputFile>', 'Path and name of file to write service names.')
        print '\n\t{:<20}: {}'.format('{OVERWRITE|APPEND}', 'Overwrite or append to existing file. Default is to overwrite.\n')
        return None
    
    else:
        
        # Set variables from parameter values
        portal_url = sys.argv[1]
        user = sys.argv[2]
        password = sys.argv[3]
        output_file = sys.argv[4]
        access_mode = 'OVERWRITE'
        
        if len(sys.argv) == 6:
            access_mode = sys.argv[5]
        
        if len(sys.argv) > 6:
            print '\nError: too many parameters.\n'
            return None
        
        valid_access_modes = ['OVERWRITE', 'APPEND']
        if not access_mode.upper() in valid_access_modes:
            print '\nError: incorrect access mode "{}". Valid choices are {}\n'.format(access_mode, valid_access_modes)
            return None
        
        if access_mode.upper() == 'OVERWRITE':
            access_mode = 'w'
        else:
            access_mode = 'a'
    
    return portal_url, user, password, output_file, access_mode

if __name__ == "__main__":
    main()
