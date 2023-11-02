### NSQ
```bash
# Publish message
curl -d "@message.json" http://nsqd-1:4151/pub?topic=training-rust
# Get Messagse
# In any nsq container, run nsq_tail
nsq_tail --lookupd-http-address=nsqlookupd-1:4161 --topic=training-node
```