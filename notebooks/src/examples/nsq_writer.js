const nsq = require('nsqjs')

const w = new nsq.Writer('vagrant.sravz.com', 4150)

w.connect()

w.on('ready', () => {
  w.publish('test', 'it really tied the room together')
  w.deferPublish('test', ['This message gonna arrive 1 sec later.'], 1000)
  w.publish('test', [
    'Uh, excuse me. Mark it zero. Next frame.',
    'Smokey, this is not \'Nam. This is bowling. There are rules.'
  ])
  w.publish('test', 'Wu?',  err => {
    if (err) { return console.error(err.message) }
    console.log('Message sent successfully')
    w.close()
  })
})

w.on('closed', () => {
  console.log('Writer closed')
})