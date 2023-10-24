FROM node:18-alpine

COPY . /app

WORKDIR /app

CMD npm RUN src/index.js 


#RUN pip install pandas

#RUN /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

#RUN (echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/anirud/.zprofile

#RUN eval "$(/opt/homebrew/bin/brew shellenv)"

#RUN brew install mongodb-atlas

#RUN pip install mysql-connector-python

#RUN xcode-select --install

#ENV PORT = 5500


#RUN npm install

#EXPOSE 5500

#CMD ["npm", 'start']

#RUN pip install -U scikit-fuzzy

#RUN pip install matplotlib

#RUN pip install numpy
