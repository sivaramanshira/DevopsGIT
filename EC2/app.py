import matplotlib.pyplot as plt
import base64
from io import BytesIO




positvepercent = 35
negativepercent = 40
neutralpercent = 25


cars = ['Jenkins','Docker','GIT']

data = [positvepercent,negativepercent,neutralpercent]

    # Creating plot
fig = plt.figure(figsize =(10, 7))
    #plt.pie(data, labels = data)
plt.pie(data, autopct='%1.1f%%',  startangle=90)

plt.legend(title="#JenkinsIntegrationTask",labels= cars, loc="best")

tmpfile = BytesIO()
fig.savefig(tmpfile, format='png')
encoded = base64.b64encode(tmpfile.getvalue()).decode('utf-8')

html = 'Jenkins Integration with Docker in EC2 instance' + '<img src=\'data:image/png;base64,{}\'>'.format(encoded) + 'Created by Sivaraman'

with open('/var/www/html/index.html','w') as f:
    f.write(html)
plt.show()
