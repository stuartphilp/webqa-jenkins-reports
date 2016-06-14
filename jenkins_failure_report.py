import simplejson as json
import requests
import datetime

overview = requests.get('https://webqa-ci.mozilla.com/api/json')

overview_json = json.loads(overview.text)

for job in overview_json["jobs"]:

  if job["color"] == "red":

    job_request = requests.get('https://webqa-ci.mozilla.com/job/%s/api/json' % job['name'])
    job_json = json.loads(job_request.text)

    last_build_num = job_json["lastBuild"]["number"]
    last_successful_num = job_json["lastSuccessfulBuild"]["number"]

    failing_build_count = 0

    if last_build_num > last_successful_num:
      failing_build_count = last_build_num - last_successful_num

    print "\n\n%s is failing and has been failing for %s build(s)" % (job['name'], failing_build_count)

    print "==========================="
    print "FAILURES"
    print "==========================="
    build_id = last_build_num
    for i in range(failing_build_count):
      failing_job_request = requests.get('https://webqa-ci.mozilla.com/job/%s/%s/api/json' % (job['name'], build_id))
      failing_job_json = json.loads(failing_job_request.text)
      claims = failing_job_json['actions'][9]
      if 'reason' in claims.keys():
        print "==========================="
        print "Job ID: %s" % build_id
        print "==========================="
        print "Reason: %s" % claims['reason']
        print "Claimed: %s" % claims['claimed']
        print "Claimed By: %s" % claims['claimedBy']

        if claims['claimDate']:
          claim_date = datetime.datetime.fromtimestamp(float(claims['claimDate']/1000)).strftime('%Y-%m-%d %H:%M:%S')
          print "Claimed On: %s" % claim_date

        build_id = build_id - 1
      else:
        print "==========================="
        print "No claims data found for job"
        print "==========================="

