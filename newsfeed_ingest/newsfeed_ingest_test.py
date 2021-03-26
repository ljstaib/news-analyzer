#!/usr/bin/python3
# ========================================================================
# Luke Staib ljstaib@bu.edu 
# Copyright @2021, for EC500: Software Engineering
# News Analyzer Testing
# ========================================================================

# ========================================================================
# Import newsfeed_ingest.py
# ========================================================================

# files = ["Sample.txt", "DONOTREAD.docx", "WhiteHouseBriefing.pdf"] #Sample list
from newsfeed_ingest import *

# ========================================================================
# Newsfeed Ingest Testing
# ========================================================================

def test_DiscoverContent():
	assert DiscoverContent("election") == [['The assessment was the intelligence community’s most comprehensive look at foreign efforts to interfere in the election.', 'The Treasury Department accused seven Ukrainians of working with a Russian agent “to spread misleading and unsubstantiated allegations” about President-elect Joseph R. Biden Jr.', 'See full results and maps from the Louisiana special primary elections.', 'But that may not be a good sign after all.', 'The promise of universal suffrage has animated the city’s politics for decades. Beijing’s latest moves could finally extinguish that hope.', 'In the fourth attempt, neither Prime Minister Benjamin Netanyahu nor his opponents have a clear path to power. An Islamist party has emerged as a possible kingmaker.', 'Many Israelis feel numbed by their endless election cycle. Many Palestinians are excited about a rare chance to vote — but others expect little change without statehood.', 'Israelis will vote again on Tuesday, seeking to end a political deadlock that has gripped the country for two years. This is what you need to know.', 'Voters choosing regional governments in southwestern states punished the conservative party of Chancellor Angela Merkel after a series of scandals.', 'The candidate and the man who prosecutors say recruited him to play spoiler in a Florida Senate race last year were both arrested this week.', 'Guy-Brice Parfait Kolélas, the main opposition candidate in the Republic of Congo, gave his final speech from his hospital bed, urging his fellow citizens to vote to expel an entrenched government.', 'New rules imposed by Beijing will make it nearly impossible for democracy advocates in the territory to run for chief executive or the legislature.', 'After one of the closest contests in American history, the House must now decide whether to unseat Mariannette Miller-Meeks, a Republican.', 'For years, right-wing populists have been a driving force in the Netherlands. But this week a pan-European party called Volt shook things up.', 'Trump urges his backers to vote in the Georgia runoffs — after Loeffler backs his bid to overturn the election in the Senate.', 'China’s national legislature disclosed plans for a law that would make it extremely difficult for Beijing’s critics to hold elective office in Hong Kong.', 'New proposals by the G.O.P.-controlled Legislature have targeted Sunday voting, part of a raft of measures that could reduce the impact of Black voters in the state.', 'The Senate Rules Committee is hearing testimony on a federal elections overhaul to expand voting rights.'], ['https://www.nytimes.com/2021/03/16/us/politics/election-interference-russia-2020-assessment.html', 'https://www.nytimes.com/2021/01/11/us/politics/sanctions-giuliani-trump-ukraine-election-disinformation.html', 'https://www.nytimes.com/interactive/2021/03/20/us/elections/results-louisiana-primary-elections.html', 'https://www.nytimes.com/2021/03/17/opinion/israel-election-biden.html', 'https://www.nytimes.com/2021/03/20/world/asia/hong-kong-elections-democracy.html', 'https://www.nytimes.com/2021/03/24/world/middleeast/israel-election-raam.html', 'https://www.nytimes.com/2021/03/21/world/middleeast/israel-palestinians-elections.html', 'https://www.nytimes.com/2021/03/17/world/middleeast/israeli-election.html', 'https://www.nytimes.com/2021/03/14/world/europe/germany-elections.html', 'https://www.nytimes.com/2021/03/19/us/florida-senate-race-fraud.html', 'https://www.nytimes.com/2021/03/22/world/africa/republic-of-congo-election-Kolelas.html', 'https://www.nytimes.com/2021/03/11/world/asia/china-hong-kong-elections.html', 'https://www.nytimes.com/2021/03/23/us/politics/house-iowa-election.html', 'https://www.nytimes.com/2021/03/19/world/europe/netherlands-elections-volt.html', 'https://www.nytimes.com/2021/01/05/us/politics/trump-georgia-voters.html', 'https://www.nytimes.com/2021/03/04/world/asia/china-hong-kong-election-law.html', 'https://www.nytimes.com/2021/03/06/us/politics/churches-black-voters-georgia.html', 'https://www.nytimes.com/video/us/politics/100000007671878/people-act-live-voting-rights.html'], ['The New York Times', 'The New York Times', 'The New York Times', 'The New York Times', 'The New York Times', 'The New York Times', 'The New York Times', 'The New York Times', 'The New York Times', 'The New York Times', 'The New York Times', 'The New York Times', 'The New York Times', 'The New York Times', 'The New York Times', 'The New York Times', 'The New York Times', 'AP']]
	assert DiscoverContent(1) == False
	assert DiscoverContent(True) == False

# def test_DisplayContent():
# 	assert DisplayContent(["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"]) == True

# def test_OrganizeContent():
# 	assert OrganizeContent(["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"], "Alphabetical") == ["https://en.wikipedia.org/wiki/Sun", "https://solarsystem.nasa.gov/solar-system/sun/overview/"]
# 	assert OrganizeContent(["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"], "Latest Uploaded") == ["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"]
# 	assert OrganizeContent(["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"], "Most Relevant") == ["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"]
# 	assert OrganizeContent(["https://solarsystem.nasa.gov/solar-system/sun/overview/", "https://en.wikipedia.org/wiki/Sun"], "Something Else") == False

# def test_ReadLater():
# 	assert ReadLater(10, "0010") == False
# 	assert ReadLater(0, "0001") == False
# 	assert ReadLater(0, "0010") == "0010"

def test_DiagnosticsNewsfeed():
	assert DiagnosticsNewsfeed() == True
  