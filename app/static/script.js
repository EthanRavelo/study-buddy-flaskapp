var rainaudio = new Audio('rain.mp3');
    rainaudio.volume = 0;
    rainaudio.loop = true;
    var oceanaudio = new Audio('ocean.mp3');
    oceanaudio.volume = 0;
    oceanaudio.loop = true;
    var lofiaudio = new Audio('lofi.mp3');
    lofiaudio.volume = 0;
    lofiaudio.loop = true;

    const volumeSlider1 = document.getElementById('myRange1');
    volumeSlider1.addEventListener('input', (e) => {
      const value1 = e.target.value;
      oceanaudio.volume = value1 / 100;
    });

    const volumeSlider2 = document.getElementById('myRange2');
    volumeSlider2.addEventListener('input', (e) => {
      const value2 = e.target.value;
      rainaudio.volume = value2 / 100;
    });

    const volumeSlider3 = document.getElementById('myRange3');
    volumeSlider3.addEventListener('input', (e) => {
      const value3 = e.target.value;
      lofiaudio.volume = value3 / 100;
    });

    function play() {
      rainaudio.play();
      oceanaudio.play();
      lofiaudio.play();
    }