# playwright_automation
This script is like a little robot for your web browser. It's designed to:

Log in for you: It remembers your login so you don't have to type it in every time.

Click around: It automatically goes through a few menus to find a specific page with product information.

Collect data: It looks at a table of products and saves all the information. It can even handle pages with lots of data that are split up.

Make a file: It puts all the collected data into a nice, organized file called products.json.

How to get started
First, you need to make sure you have Python installed on your computer. Then, you need to install a tool called Playwright.

Open your command line or terminal.

Type the following command and hit Enter:

pip install playwright

Next, you need to download the browser tools. Type this and hit Enter:

playwright install

Important things to change in the script
Before you run the script, you have to tell it about the website you're using.

Open the product_scraper_v2.py file and find these lines to replace them with your own information:

Your login details:

Change "your-username" to your actual username.

Change "your-password" to your actual password.

The website addresses:

Update the login page address and the dashboard address to match the website you're using.

The buttons and menus:

You might need to change the names of the buttons it clicks to find the product table.

How to run the script
Once you've made those changes, it's easy! Just go back to your terminal and run this command:

python product_scraper.py

After it's done, you'll see a new file called products.json that has all the product data inside.

Hope this helps!
