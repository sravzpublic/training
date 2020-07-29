// npm install nsqjs
// copy this file where node_modules is located and then run node nsq_reader.js
const nsq = require('nsqjs')

const reader = new nsq.Reader('test', 'test_channel', {
  lookupdHTTPAddresses: 'localhost:4161'
})

reader.connect()

reader.on('message', msg => {
  console.log('Received message [%s]: %s', msg.id, msg.body.toString())
  msg.finish()
})