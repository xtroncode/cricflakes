#!/usr/bin/python

import xmltodict,json
try:
    import urllib.request as urllib2
except:
    import urllib2

class CricbuzzParser():
    
    def __init__(self):
       
        pass
       
    def getJson(self):
        #Change coding here
        f = urllib2.urlopen("http://synd.cricbuzz.com/j2me/1.0/livematches.xml")
        doc = xmltodict.parse(f)
        node = doc['mchdata']
        matches = node["match"]
        return matches

    def handleMatches(self,matches):
        """This function handles the element <match> and
        avoids duplicate matches to be processed. """
        duplicate = []
        match_details = []
        mchDesc = matches[0]["@mchDesc"]
        duplicate.append(mchDesc)
        if matches[0]['@type'] != "TEST":
          match_detail = self.handleMatch(matches[0])
          match_details.append(match_detail)
        else:
          match_detail = self.handleTestMatch(matches[0])
          match_details.append(match_detail)
        for match in matches:
            flag = False
            mchDesc = match["@mchDesc"]
            #If list duplicate is empty, then populate it initially.
            for entry in duplicate:
                if entry == mchDesc: #If duplicate is found
                    flag = True
            if flag is not True:
                duplicate.append(mchDesc)
                if match['@type'] != "TEST":
                  match_detail = self.handleMatch(match)
                  match_details.append(match_detail)
                else:
                  match_detail = self.handleTestMatch(match)
                  match_details.append(match_detail)
        return match_details

    def handleTestMatch(self,match):
        """For handling Test Matches.
        To Do: Write Code for Parsing Innings detail"""
        series = match["@srs"]
        mtype = match["@type"]
        if mtype != "TEST":
            return None
        else:
            match_desc = match["@mchDesc"]
            mground = match["@grnd"]
            states = match["state"]
            for state in states:
                match_cstate = state["@mchState"]
                mstatus = state["@status"]
                if mstatus.startswith("Starts") or mstatus.startswith("Coming"):
                    return None       #Match hasn't started Yet.
        html="<li><p>{3}<p><p>{0}<p><p>{1}<p><p>{2}<p></li>".format(match_desc,mground,match_cstate,mstatus,mtype)
        return html
                
            
    def handleMatch(self,match):
        """Handles ODI and T20 matches"""
        bowl_runs  = None
        bowl_wkts = None
        bowl_overs = None
        series = match["@srs"]
        mtype = match["@type"]
        if mtype == "TEST":
            return None
        match_desc = match["@mchDesc"]
        mnum=match['@mnum']
        states = match["state"]
        match_cstate = states["@mchState"]
        mstatus = states["@status"]
        inngCnt=match['@inngCnt']
        if mstatus.startswith("Starts") or mstatus.startswith("Coming"):
          return None       #Match hasn't started Yet.
        if match_cstate=="Result":
          mom=match['manofthematch']
          mom_num_player=int(mom['@NoOfPlayers'])
          mom_pname=""
          for i in range(mom_num_player):
            mom_pname+=mom['mom']['@Name']
          html="<li><p>{0} | {1} | {2} | {6}</p><p>{3} : {4}</p><p>Man of the Match: {5}</p></li>".format(series,mtype,match_desc,match_cstate,mstatus,mom_pname,mnum)
          return html
        try:
            batting_team = match['mscr']["btTm"]
            bowling_team = match['mscr']["blgTm"]
            batting_team_name = batting_team["@sName"]
            bowling_team_name = bowling_team["@sName"]
            innings = match['mscr']['btTm']["Inngs"]
            bat_runs = innings["@r"]
            bat_overs = innings["@ovrs"]
            bat_wkts = innings["@wkts"]
        except Exception:
            
            pass
        try:
            bowl_runs = bowling_team['Inngs']["@r"]
            bowl_overs = bowling_team['Inngs']["@ovrs"]
            bowl_wkts = bowling_team['Inngs']["@wkts"]
        except Exception:
            # The opponent team hasn't yet started to Bat.
            pass
        html="<li><p>{0} | {1} | {2}<p>{3} | {4}<p>Batting:</p><p class='score'>{5}:{6}-{7} / {8} ovrs</p>".format(series,mtype,match_desc,match_cstate,mstatus,batting_team_name,bat_runs,bat_wkts,bat_overs)
        if inngCnt=='2':
          html+="<p>Bowling:</p><p class='score'>{0}:{1}-{2} / {3} ovrs</p></li>".format(bowling_team_name,bowl_runs,bowl_wkts,bowl_overs)
        else:
          html+="</li>"
        return html
if __name__ == '__main__':
    cric = CricbuzzParser()
    match = cric.getXml()
    details = cric.handleMatches(match) #Returns Match details as a Dictionary. Parse it according to requirements.
    details={'details':details}
    details=json.dumps(details)
    print (details)
    
