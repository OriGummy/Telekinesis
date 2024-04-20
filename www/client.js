HOSTNAME = "10.10.10.31"
HTTP_PORT = 5000
WS_PORT = 8001
BASE_URL = "http://" + HOSTNAME + ":" + HTTP_PORT + "/"
WS_URL = "ws://" + HOSTNAME + ":" + WS_PORT


function get_id(){
  if (document.cookie == ""){
    document.cookie = Math.floor(Math.random() * 100000000);
  }
  console.log("Cookie is", document.cookie)
  return document.cookie;
}

function listen_for_actions(){
  console.log("Connecting to " + WS_URL)
  ws = new WebSocket(WS_URL)

  ws.onopen = () => {
    console.log("Connected")
    ws.send('{"display": true, "id": ' + get_id() + '}')
  }

  ws.onclose = () => {
    console.log("Disconnected")
    setTimeout(() => {
      listen_for_actions()
    }, 1000)
  }
  ws.onmessage = (event) => {
    action = event.data
    console.log('Action: ' + action)
    const body = document.querySelector('body');

    body.style.backgroundImage = "url('"+ BASE_URL + action +"')";
    body.style.backgroundSize = "cover";
    body.style.backgroundRepeat = "no-repeat";
    body.style.backgroundPosition = "top bottom";
  }
}


listen_for_actions()