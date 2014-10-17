redirects = {
    "resumes-by-week-joined":"select \
      str_to_date(concat(yearweek(date_joined),' Saturday'),'%X%V %W') as YearWeekJoined, \
      case \
        when profile_completion = 0 then '0' \
        when profile_completion < 26 then '1-25' \
        when profile_completion < 51 then '26-50' \
        when profile_completion < 76 then '51-75' \
        else '76-100' \
      end as ResumeCompletion, \
      count(*) as ProfileCount \
    from myjobs_user WHERE date_joined >= DATE_SUB(NOW(),INTERVAL 1 YEAR) \
    group by YearWeekJoined, ResumeCompletion \
    order by YearWeekJoined, ResumeCompletion;",

    "binary-resumes":"SELECT  STR_TO_DATE(CONCAT(YEARWEEK(date_joined),' \
        Saturday'),'%X%V %W') AS YearWeekJoined, \
        COUNT(CASE WHEN profile_completion > 0 THEN profile_completion END) AS Resume, \
        COUNT(CASE WHEN profile_completion = 0 THEN profile_completion END) AS NoResume \
        FROM myjobs_user \
        WHERE date_joined >= DATE_SUB(NOW(),INTERVAL 1 YEAR) \
        GROUP BY YearWeekJoined \
        ORDER BY YearWeekJoined",

    "saved-searches-by-group":"SELECT \
        STR_TO_DATE(CONCAT(YEARWEEK(ss.created_on),' Saturday'),'%X%V %W') \
        as YearWeekJoined, \
        CASE SUBSTRING_INDEX(SUBSTRING_INDEX(ss.url,'/', 3),'/',-1) \
        WHEN 'my.jobs' THEN 'redirect' \
        WHEN 'www.my.jobs' THEN 'www.my.jobs' \
        ELSE 'network' \
        END AS Hostname, \
        COUNT(distinct ss.user_id) AS CountJoined \
        FROM mysearches_savedsearch ss \
        JOIN myjobs_user u ON ss.user_id = u.id \
        WHERE u.email LIKE '%@%' \
        AND DATE(u.date_joined) = DATE(ss.created_on) \
        AND  date_joined >= DATE_SUB(NOW(),INTERVAL 1 YEAR) \
        GROUP BY YearWeekJoined, Hostname \
        ORDER BY YearWeekJoined DESC;",

    "accounts-by-week":"select str_to_date(concat(yearweek(`date_joined`),' \
        Saturday'),'%X%V %W') as YearWeekJoined, count(*) as JoinedCount \
        FROM myjobs_user \
        WHERE date_joined >= DATE_SUB(NOW(),INTERVAL 1 YEAR) \
        group by YearWeekJoined order by YearWeekJoined DESC"
}
