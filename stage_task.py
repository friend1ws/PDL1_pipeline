#! /usr/bin/env python

import os
import sys
import datetime
import subprocess
import drmaa

file_timestamp_format = "{name}_{year:0>4d}{month:0>2d}{day:0>2d}_{hour:0>2d}{min:0>2d}_{msecond:0>6d}"

class Stage_task(object):

    def __init__(self, qsub_option):
        self.qsub_option = qsub_option
        self.retry_count = 2


    def task_exec(self, arguments, script_dir, log_dir, max_task = 0):
        # Make shell script

        now = datetime.datetime.now()
        shell_script_name = file_timestamp_format.format(
                                 name=self.task_name,
                                 year=now.year,
                                 month=now.month,
                                 day=now.day,
                                 hour=now.hour,
                                 min=now.minute,
                                 msecond=now.microsecond )
        
        shell_script_full_path = "{script}/{file}.sh".format(script = script_dir, file = shell_script_name)
        shell_script_file = open(shell_script_full_path, 'w')
        shell_script_file.write(self.script_template.format(**arguments))
        shell_script_file.close()

        
        s = drmaa.Session()
        s.initialize()
    
        jt = s.createJobTemplate()
        jt.jobName = shell_script_name
        jt.outputPath = ':' + log_dir
        jt.errorPath = ':' + log_dir
        jt.nativeSpecification = self.qsub_option
        jt.remoteCommand = shell_script_full_path
        os.chmod(shell_script_full_path, 0750)

        returncode = 0
        if max_task == 0:
            for var in range(0, (self.retry_count+1)):
                jobid = s.runJob(jt)
                returncode = 0
                now = datetime.datetime.now()
                date = now.strftime("%Y-%m-%d %H:%M")
                print >> sys.stderr, "Date/Time: " + date 
                print "Job has been submitted with id: " + jobid + " at Date/Time: " + date
                retval = s.wait(jobid, drmaa.Session.TIMEOUT_WAIT_FOREVER)
                now = datetime.datetime.now()
                date = now.strftime("%Y-%m-%d %H:%M")
                print >> sys.stderr, "Job: " + str(retval.jobId) + ' finished with status: ' + str(retval.hasExited) + ' and exit status: ' + str(retval.exitStatus) + " at Date/Time: " + date
                returncode = retval.exitStatus
                if returncode == 0: break
            s.deleteJobTemplate(jt)
            s.exit()

