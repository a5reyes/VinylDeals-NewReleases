# VinylDeals-NewReleases
Dec '24 - Present
website: https://reyesalbert34.pythonanywhere.com/

get new releases from vinylreleases subreddit

-get deals from vinyldeals sub

-sort by/rank by:
price, number of lps, size of lp(10", 12", 7")

-set limit to amount of releases or deals you want to see

update 1/20/25 - now removes expired vinyl deals, added buttons for links, added my amazon affiliate sitestripe tag to amazon deals

update 1/21/25 - removing expired vinyl deals takes way too much time, will work on that, fixed button links & displays, also changed price sorting from list + dict to strictly dicts only in order to not have any duplicates of any releases after sorting by price and also to sort more precisely

update 1/26/25 - fixed the removing expired vinyl deals part using list + bool and added images for deals

update 2/1/25 - fixed removing expired vinyl deals part using the flair text on posts instead of comments as from tests, i found that most of the deals are listed as expired mostly through the post's flair. I still use a list for expired posts. included a url checker method to make sure all the externals urls are valid. changed the styling of the page. replaced www links with https
