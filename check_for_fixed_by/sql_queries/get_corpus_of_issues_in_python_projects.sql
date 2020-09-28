CREATE TEMP FUNCTION json2array(json STRING)
RETURNS ARRAY<STRING>
LANGUAGE js AS """
function parseLabels(x) {
    return JSON.stringify(x.name);
}
var row = JSON.parse(json);
return row.map(x => parseLabels(x));
""";

select a.url, a.repo_name, a.labels, a.action from (
    SELECT url, repo_name, labels, action FROM (
        SELECT repo.name as repo_name, JSON_EXTRACT(payload, '$.issue.html_url') as url, json2array(JSON_EXTRACT(payload, '$.issue.labels')) as labels,
        JSON_EXTRACT(payload, '$.action') as action
        From `githubarchive.day.201*`
        WHERE _TABLE_SUFFIX between "50101" and "90101" and type = 'IssuesEvent'
        ), UNNEST(labels) as l where action= "\"closed\"" and not REGEXP_CONTAINS(l,'(D|d)ebug') and REGEXP_CONTAINS(l,'(B|b)ug')
) as a Inner Join `python_project_repos` as b on a.repo_name = b.repo_name order by RAND()


-- NOTE 'python_project_repos' is the table that contains all of python projects in Github. Our version of the repository is location at a temp location of 'youtube-test-player-1379.github_issues.python_project_repos'.

-- This query should only be run after get_python_projects.sql is executed.