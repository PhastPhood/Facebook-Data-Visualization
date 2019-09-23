# Facebook-Data-Visualization
This repo contains script(s) to run on your downloaded data from facebook. It aims to offer fun data visualizations from your past messenger messages, posts, and whatever else.

See The following link to download your data.
https://www.facebook.com/help/1701730696756992?helpref=hc_global_nav

To use, download and install Python 3 [here](https://www.python.org/downloads/).

Then, run the following command in the command line to install matplotlib:
```
pip3 install matplotlib
```

### Plot Messenger Messages

See who you talk to over time.

Takes a path to your messages inbox folder. Takes in your name, the recipient's name, maximum group text size, and minimum number of messages in order to display.

```
`python3 plot_messages.py ~/Downloads/facebook/messages/inbox/ --recipient 'Other Name' --name 'My Name' --messages 50 --maxgroup 10`
```
