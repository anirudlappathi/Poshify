FROM node:18-alpine
WORKDIR /app
COPY . .
RUN pip install pandas 
RUN pip install mysql-connector-python
CMD ["node", 'src/index.js']
EXPOSE 5500
