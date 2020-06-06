
Stock investing, if done properly, yield better returns over the long term compared to other conservative investment vehicles. The success comes from choosing the stocks with solid fundamentals out of thousands. However, finding these stocks is as difficult as finding a unicorn. Picking a fundamentally sound stock involves investigating stocks from different angles such as evaluating fundamental ratios, company management analysis, product impact in the consumer market, about its competitors, and many more. Every step is crucial in deciding the stock we want to invest in and each part demands a substantial amount of time. So doing these steps on every stock is not a good idea. We have to choose only a handful of potential stocks based on certain criteria usually set on performance indicators. But reviewing fundamentals for current year does not reveal much information and sometimes might be misleading because for some reason situation be different in that financial year. Instead, we need to take a look at performance indicators over past few years to get a clear picture of the company's performance.

This project tries to make the initial stocks screening process and the most important aspect i.e reviewing the trend of performance indicators easier. Reviewing company fundamentals involves understanding how well the company has performed over the past few years by looking at annual figures and also the trend. Again, doing that manually is a hectic job as it involves collecting the list of stocks that meet our criteria, going over each stock page that is in our screened stock list, fetching historical data of performance indicators, and maybe plotting them to understand its trend. So, I decided to build a Web Crawler in **python** that does all these tasks at one go. To sum it up, the objective of this project is to help users choose best value stocks thereby allowing them to screen stocks based on criteria set by them and perform detailed historical performance review on the selected stocks. The code is available on my GitHub [repo](https://github.com/Skumarr53/Stock-Fundamental-data-scraping-and-analysis) 

## Files Description

1. Stock_FundamentalPlots.ipynb - Ipython Notebook that crawls through the list of stock pages and collects the historical data for selected performance indicators

2. TrendPlots - Output directory where generated plots will be saved.


## Approach:

 This approach involves the following steps:
 1. Logging into a data provider server.
 2. Submitting the query that filters the stocks qualifying our criteria
 3. Collecting the stocks links storing in the list from current first page (if results exceeded more than a page).
 4. Looping over the collected stock links and fetching required data, and simultaneously generating Plots for every link.
 5. Move to the next page and repeat steps 3-4 till the last page.

Requirements:
1. Python: the Web crawler is built in Python
2. Selenium: a tool that interacts with the webserver on the backend
3. Beautifulsoap: a package that helps to fetch data from HTML document
4. Numpy: Raw data which is text format is converted and stored in a numeric array format
5. Matplotlib: Plots Generation

## Step wise implementation
1. In this step, we initialize the selenium web driver to log in to the web server by submitting user credentials. Screener.in is the data source and the Login link is provided below. https://www.screener.in/login/

<img class="ez um s t u el ai kx" width="933" height="470" srcset="https://miro.medium.com/max/552/1*XmWgkwVtxSD5nPtyfuBJAQ.png 276w, https://miro.medium.com/max/1104/1*XmWgkwVtxSD5nPtyfuBJAQ.png 552w, https://miro.medium.com/max/1280/1*XmWgkwVtxSD5nPtyfuBJAQ.png 640w, https://miro.medium.com/max/1400/1*XmWgkwVtxSD5nPtyfuBJAQ.png 700w" sizes="700px" role="presentation" src="https://miro.medium.com/max/840/1*XmWgkwVtxSD5nPtyfuBJAQ.png">

2. Once we successfully get inside the server now we have access to the data. now we can run our query to filter the stock that passes our criteria. I have set a simple query 'market capitalization > 0'. After running this query it lists out all the companies that have a market capitalization above zero. Below is the screenshot of the resulting page.

query link: https://www.screener.in/screen/raw/?sort=&source=&order=&page=1&query=Market+Capitalization%3E0

<img class="ez um s t u el ai kx" width="1000" height="331" srcset="https://miro.medium.com/max/552/1*pDSROishJhHP_YJh9tURDA.png 276w, https://miro.medium.com/max/1104/1*pDSROishJhHP_YJh9tURDA.png 552w, https://miro.medium.com/max/1280/1*pDSROishJhHP_YJh9tURDA.png 640w, https://miro.medium.com/max/1400/1*pDSROishJhHP_YJh9tURDA.png 700w" sizes="700px" role="presentation" src="https://miro.medium.com/max/900/1*pDSROishJhHP_YJh9tURDA.png">

Note there are 3879 results passed our criteria and they are stored across 156 pages. We need to embedd the page number in the query link  at "&page=1&" to crawl across the pages 1-156 to fetch all the resulted stock links. Currently, we are on page 1, let's collect all the stock page links and store them in the list. the links can be scraped by extracting 'href' tags associated with stock links using the 'bs4' package. We need to visit each stock page to source the data from it. It's done by creating beautifulsoup object of page, then locating tags that correspond to the data we are interested in and storing the data in an array format. Below is the example, glance of the web page.

<img class="ez um s t u el ai kx" width="831" height="386" srcset="https://miro.medium.com/max/552/1*J-jdz7dIm6_vhcXa6qTx7A.gif 276w, https://miro.medium.com/max/1104/1*J-jdz7dIm6_vhcXa6qTx7A.gif 552w, https://miro.medium.com/max/1280/1*J-jdz7dIm6_vhcXa6qTx7A.gif 640w, https://miro.medium.com/max/1400/1*J-jdz7dIm6_vhcXa6qTx7A.gif 700w" sizes="700px" role="presentation" src="https://miro.medium.com/max/748/1*J-jdz7dIm6_vhcXa6qTx7A.gif">

The page contains several tables of indicatiors historical data that describe the past performance and financial health of the company. But I have considered only a few indicators based on my intuition that decides the stability and profitability of a company in the competitive environment in the long run. You will see the selected indicators on the plot generated in a while.

Collecting just numbers won't tell much as it is difficult to interpret just looking at the numbers. We can create visual plots on the fly which tells the story about the company and may give hints about where it is heading in the future. Below I have added a trend plot of performance indicators for Avanti Feeds Ltd company as an example case. The company is mainly into aquacultural feed manufacturing business along with the production of value-added products of shrimps.

<img class="ez um s t u el ai kx" width="1000" height="746" srcset="https://miro.medium.com/max/552/0*xoT2BTVs0pgWhI-Q.png 276w, https://miro.medium.com/max/1104/0*xoT2BTVs0pgWhI-Q.png 552w, https://miro.medium.com/max/1280/0*xoT2BTVs0pgWhI-Q.png 640w, https://miro.medium.com/max/1400/0*xoT2BTVs0pgWhI-Q.png 700w" sizes="700px" role="presentation" src="https://miro.medium.com/max/900/0*xoT2BTVs0pgWhI-Q.png">

I will present here some of my insights about its management. Let's go over them.

1. Sales growth - The company has aggressively expanded its sales (>50%) but it dropped in recent years suggest that the company is close to attaining market saturation. But still, It has maintained above 25 % most of the financial years.

2. Operating profit Margin - The operating margin shows positive trend. It signifies the difference between sales revenue and product manufacturing cost growing over years. Notice that there is a sharp rise in 2017 which can be attributed to a drop in raw materials price. Also, drop-in current years can be attributed to the rise in raw materials price above normal range found out upon doing some research.

3. Net profit growth - This has the same story as the above. The company Net profit margin in recent years is close to 8-9% which is a decent number. Company profit showing a positive trend is a good sign.

4. Asset Purchased - Asset purchase can be associated with business expansion or improvements such as replacing existing, entering into a new market segment or new business. A significant positive value indicates the company is growing.

5. Reinvestment into Business - Reinvestment into Business is almost the same as the previous one but expressed in the percentage of sales revenue. This will give a better picture of the company's growth. Suppose, there are two companies A and B of market capitalization 100 cr and 1000 cr. Both companies Reinvesting 10 cr into the business are not the same. A is expanding in business by 10% whereas B is expanding by only 1%. A is more aggressive when compared to B. The Avanti Feeds has maintained above 10% most of the years which are a good number for a company of this size.

6. Return on Capital employed - Idea is generally capital invested should yield higher percent returns or else the company is not making the best use of its resources. Its a loose indicator need not be taken seriously because capital invested this year may not get converted into returns the same year but in the long run yield good returns. So investors should focus long term trends rather than just numbers.

7. Free cash flows - It is the cash left with the company after deducting tax paid, capital expenditure, and networking capital from earnings. This is the actual cash available to owners, shareholders, and lenders. Hence, This number more meaningful than net profit in terms of business returns and it forms the base input for stock price evaluation. Avanti Feeds has shown an increasing trend however actual number also matters.

8. Debt - Debt is one of the factors that decide the stability of the company if not keep under control may lead to the downfall of the company in a weak economy. An increasing trend tells that the company is struggling to meet its financial needs. This company is almost free from debt, which is good.

9. EPS - Earnings per share is the profit earned by shareholders per share. From 2011 onwards the EPS value is monotonically increasing till 2018 which means the investors have a positive sentiment towards the company and confident about the company's growth in the future. It seems likes a drop in the Sale growth and profit margins in the 2019 financial year may have negatively impacted EPS.  

These insights just scratch the surface there is more to it like understanding interactions between indicators for better insights. Reading plots and developing a story is an art that can be mastered by practice and experience. It is advised to go over the past few year financial reports to know the actual reasons behind changes observed in plots.

Now we scraped data for the first company in the first page. This task has to be repeated for all the stock links in the page, then move on to the second page and so on in iterative manner.

Let's put our webcrawler into action. For demonstration purpose I made to the crawler to login into the source, visit first three pages and in every page, its performs scraping on the first three stock links, and log out from the source. Below is a clip of it.

<img class="ez uw s t u el ai kx" width="720" height="405" srcset="https://miro.medium.com/max/552/1*sQ0tbbvbc-tmMqwpovDWrw.gif 276w, https://miro.medium.com/max/1104/1*sQ0tbbvbc-tmMqwpovDWrw.gif 552w, https://miro.medium.com/max/1280/1*sQ0tbbvbc-tmMqwpovDWrw.gif 640w, https://miro.medium.com/max/1400/1*sQ0tbbvbc-tmMqwpovDWrw.gif 700w" sizes="700px" role="presentation" src="https://miro.medium.com/max/648/1*sQ0tbbvbc-tmMqwpovDWrw.gif">

Thank you for reading. Any thoughts would be appreciated.

Happy Investing.