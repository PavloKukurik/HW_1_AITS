#!/bin/bash

docker build -t book_api .

docker run -d -p 5000:5000 --name book_api_container book_api
