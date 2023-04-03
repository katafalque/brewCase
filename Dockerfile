FROM python:3.11
ADD . /app

ENV AMAZON_URL='https://www.amazon.com.tr/'
ENV AMAZON_DEPARTMENT_DROPDOWN_XPATH='//*[@id="searchDropdownBox"]/option[10]'
ENV AMAZON_SEARCHBOX_XPATH='//*[@id="twotabsearchtextbox"]'
ENV AMAZON_SEARCH_BUTTON_XPATH='//*[@id="nav-search-submit-button"]'
ENV AMAZON_FIRST_RESULT_XPATH='//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[2]/div/div/div/div/div/div[2]/div/div/div[1]/h2/a'
ENV AMAZON_BOOK_PAGESIZE_XPATH='//*[@id="rpi-attribute-book_details-fiona_pages"]/div[3]'
ENV AMAZON_BOOK_PRICE_XPATH = '//*[@id="price"]'
ENV AMAZON_BOOK_TITLE_XPATH = '//*[@id="productTitle"]'
ENV AMAZON_BOOK_ISBN_XPATH = '//*[@id="detailBullets_feature_div"]/ul/li[6]/span/span[2]'
ENV AMAZON_BOOK_ISBN_OOS_XPATH = '//*[@id="detailBullets_feature_div"]/ul/li[5]/span/span[2]'
ENV AMAZON_BOOK_AUTHOR_XPATH = '//*[@id="bylineInfo"]/span/a'
ENV AMAZON_BOOK_OOS_XPATH = '//*[@id="outOfStock"]'
ENV AMAZON_BOOK_EXIST_XPATH = '//*[@id="search"]/div[1]/div[1]/div/span[1]/div[1]/div[1]/div/div/div'
ENV GOOGLE_API_URL = 'https://www.googleapis.com/books/v1/volumes'

RUN apt-get update -y
RUN apt-get install -y libglib2.0-0 libnss3 libgconf-2-4 libfontconfig1
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list
RUN apt-get update && apt-get -y install google-chrome-stable
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/111.0.5563.64/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/


WORKDIR /app
RUN pip install -r requirements.txt


ENTRYPOINT [ "python", "cli.py" ]