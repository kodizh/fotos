<style>
  span {
    display: inline-block;
    vertical-align:middle;
    width: 100%;
    margin-bottom: 1em;
  }

  span img {
    vertical-align: middle;
    height: 5em;
    margin-right: 10px;
  }

  .container.gallery-container {
      min-height: 100vh;
      padding: 30px 50px;
  }

  .tz-gallery {
      padding: 40px;
  }

  /* Override bootstrap column paddings */
  .tz-gallery .row > div {
      padding: 2px;
  }

  .tz-gallery .lightbox img {
      width: 100%;
      height: 100%;
      object-fit: cover;
      border-radius: 0;
      position: relative;
  }

  .tz-gallery .lightbox:before {
      position: absolute;
      top: 50%;
      left: 50%;
      margin-top: -13px;
      margin-left: -13px;
      opacity: 0;
      color: #fff;
      font-size: 26px;
      font-family: 'Glyphicons Halflings';
      content: '\e003';
      pointer-events: none;
      z-index: 9000;
      transition: 0.4s;
  }


  .tz-gallery .lightbox:after {
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 100%;
      opacity: 0;
      background-color: rgba(255, 255, 255, 0.7);
      content: '';
      transition: 0.4s;
  }

  .tz-gallery .lightbox:hover:after,
  .tz-gallery .lightbox:hover:before {
      opacity: 1;
  }

  .baguetteBox-button {
      background-color: transparent !important;
  }

  input {
    width: 80%;
  }

  @media screen and (device-aspect-ratio: 375/667) {
    form input {
      font-size: 16px;
    }
  }

  @media (min-height: 845px) {
    #chatWindow {
      height: 600px;
    }
  }
</style>

<svelte:head>
  <title>Photo manager</title>
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css">
  <link rel="stylesheet" href="https://rawgit.com/LeshikJanz/libraries/master/Bootstrap/baguetteBox.min.css">
  <style>
    body {
      background: #424242;
      font: 13px "Noto Sans";
      color: #fff7da;
    }
  </style>
  <script src="https://cdnjs.cloudflare.com/ajax/libs/baguettebox.js/1.8.1/baguetteBox.min.js" on:load={baguetteBoxLoaded}></script>
</svelte:head>

<svelte:window on:unload={emitUserDisconnect}/>

<script>
  import io from "socket.io-client";
  import { fade } from "svelte/transition";
  import { afterUpdate } from 'svelte';
//  import { Col, Container, Row } from 'sveltestrap';

  const socket = io.connect({transports: ['websocket']});
  const placeholder = "Type your query here...";
  let query = "/home/pi/Pictures/abis_birthday/";
  let picslist = [];
  let plist_size = 0;
  let nbLargePics = 0;
  let baguetteBoxReady = false;

  socket.on("search_results", function(resultslist) {
    nbLargePics = 0;
    picslist = resultslist["results"];
    plist_size = resultslist["size"];
  });

	afterUpdate(() => {
    if( baguetteBoxReady ) {
      reloadResultsList();
    }
	});

  function emitUserDisconnect() {
    socket.emit('user disconnect', "");
  }

  function baguetteBoxLoaded() {
    baguetteBoxReady = true;
  }
  function handleSubmit() {
    query = query.trim();

    if (query == '') {
      return;
    }
    socket.emit("search", { "directory": query });
  }

  function getPhoto(picture) {
    return "get_photo?album="+ encodeURIComponent(picture["album"])
        +"&name="+ encodeURIComponent(picture["name"]);
  }

  function getPictureSize(picture) {
    if( nbLargePics < 1 && Math.random() < 0.25 ) {
      nbLargePics++;
      return "col-sm-12 col-md-8";
    }
    else {
      return "col-sm-6 col-md-4";
    }
  }

  function reloadResultsList() {
    baguetteBox.run('.tz-gallery')
  }
</script>

<body>
  <span>
    <img src="images/puffin_logo.png" alt="logo"/>
    <input id="m" autocomplete="off" {placeholder} bind:value={query} />
    <button on:click|preventDefault={handleSubmit}>Send</button>
  </span>
  <main class="container gallery-container">
    <div>Found {plist_size} matching photos</div>
    <div id="search_results" class="tz-gallery">
      <div class="row">
        {#each picslist as picture}
          <div class="{getPictureSize(picture)}">
            <a class="lightbox" href={getPhoto(picture)}>
              <img src={getPhoto(picture)} alt={picture["name"]} transition:fade/>
            </a>
          </div>
        {/each}
      </div>
    </div>
  </main>
</body>
