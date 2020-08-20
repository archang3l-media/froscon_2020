FROM node:14.8.0-alpine
RUN apk update && apk upgrade
RUN apk add git npm

RUN mkdir -p /revealjs
ADD reveal /
RUN npm install
#################
#Install Plugins
#################

# Install MathJax
RUN git clone https://github.com/mathjax/MathJax.git /revealjs/MathJax

# Install Menu
RUN git clone https://github.com/denehyg/reveal.js-menu.git /revealjs/plugin/menu

# Install Chalkboard
RUN mkdir -p /revealjs/plugin/chalkboard
RUN git clone https://github.com/rajgoel/reveal.js-plugins.git /revealjs/plugin/tmp && mv /revealjs/plugin/tmp/chalkboard /revealjs/plugin && rm -r /revealjs/plugin/tmp

# Install Footer
RUN mkdir -p /revealjs/plugin/footer && cd /revealjs/plugin/footer && wget https://raw.githubusercontent.com/e-gor/Reveal.js-Title-Footer/master/plugin/title-footer/title-footer.css && wget https://raw.githubusercontent.com/e-gor/Reveal.js-Title-Footer/master/plugin/title-footer/title-footer.js

# Install Charts
RUN mkdir -p /revealjs/plugin/chartjs && cd /revealjs/plugin/chartjs && wget https://gitlab.com/dvenkatsagar/reveal-chart/raw/master/plugin/chartjs/Chart.min.js && wget https://gitlab.com/dvenkatsagar/reveal-chart/raw/master/plugin/chartjs/charted.js

# Install vis.js
RUN mkdir -p /revealjs/plugin/visjs && git clone https://github.com/almende/vis.git /revealjs/plugin/visjs

ADD ./docker-entrypoint.sh /
RUN chmod u+x /docker-entrypoint.sh
EXPOSE 8000
EXPOSE 35729
CMD ["npm", "start"]