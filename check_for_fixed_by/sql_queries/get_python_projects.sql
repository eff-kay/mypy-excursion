SELECT repo_name, l.name FROM `bigquery-public-data.github_repos.languages`, UNNEST(language) as l where l.name="Python"
	
-- The temp result is available at the following public database 
-- https://bigquery.cloud.google.com/queries/youtube-test-player-1379?pli=1&tab=schema