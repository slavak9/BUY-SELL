
const PlayPauseButton = document.getElementById('button_play_pause');
const videoContent = document.querySelector('.video_player_animation_section');
const volumeValue = document.querySelector('#volume__value');
const volumeMuteValue = document.querySelector('#button_volume_mute');
const changeScreenButton = document.querySelector('#change__screen');
const videoPlayerContainer = document.querySelector('.video_player_container');
const videoPlayerControls = document.querySelector('.video_player_controls_section');
const videoDurationTime = document.querySelector('#video-duration');
const videoElapseTime = document.querySelector('#video-time-elapsed')
const videoTimeLineContainer = document.querySelector('.video_player_progress_bar_container')
const showFoundTimeLine = document.querySelector('#time-line-progress__display')
const positionPlayBt = document.querySelector('#screen__play_bt')
const subVideo = document.querySelector('#video-img-container')


//
// play pause
function togglePlay() {
    const playBT = document.getElementById('play__button');
    const pauseBT = document.getElementById('pause__button');
    if (videoContent.paused || videoContent.ended) {
        videoContent.play();
        playBT.style.display = 'none';
        pauseBT.style.display = 'initial';
        positionPlayBt.style.display = 'none';
    } else {
        videoContent.pause();
        pauseBT.style.display = 'none';
        playBT.style.display = 'initial';
        positionPlayBt.style.display = 'initial';
    }
};
PlayPauseButton.addEventListener('click', togglePlay);
videoContent.addEventListener('click', togglePlay);
positionPlayBt.addEventListener('click', togglePlay);


// position front button
function positionPlayButton() {
    const rectValue = videoPlayerContainer.getBoundingClientRect()
    let pictureWidth = Math.floor(rectValue.width / 23)
    if (rectValue.width <= 1200) { pictureWidth = 52 };
    const widthH = Math.floor(rectValue.width / 2)
    const heightH = Math.floor((rectValue.height - videoPlayerControls.getBoundingClientRect().height) / 2)
    positionPlayBt.style.setProperty('--img-width', pictureWidth)
    positionPlayBt.style.setProperty('--play-x-position', widthH - (pictureWidth / 2))
    positionPlayBt.style.setProperty('--play-y-position', heightH - (pictureWidth / 2))
    videoPlayerControls.style.setProperty('--height-aspect', Math.floor(rectValue.width) / 50)

};
videoPlayerContainer, addEventListener('resize', positionPlayButton)
videoPlayerContainer, addEventListener('load', () => {
    positionPlayButton();
    positionPlayBt.style.display = 'initial';
})

//
// change volume icon
function iconUpdateVolume(keyValue) {
    const volumeMuted = document.querySelector('#volume__mute')
    const volumeUnmuted = document.querySelector('#volume__unmute')
    const volumeMedia = document.querySelector('#volume__media')
    if (keyValue === 'mute') {
        volumeMedia.style.display = 'none'
        volumeMuted.style.display = 'none';
        volumeUnmuted.style.display = 'initial';
    } else if (keyValue === 'unmute') {
        volumeMedia.style.display = 'none'
        volumeUnmuted.style.display = 'none';
        volumeMuted.style.display = 'initial';
    } else if (keyValue === 'media') {
        volumeUnmuted.style.display = 'none';
        volumeMuted.style.display = 'none';
        volumeMedia.style.display = 'initial'
    };
};

//
// mute unmute volume
function volumeMute() {
    if (volumeValue.value == 0) {
        videoContent.volume = 0.5;
        volumeValue.value = 0.5;
        iconUpdateVolume('media')
    }
    else if (videoContent.muted) {
        videoContent.muted = false;
        videoContent.volume <= 0.5 ? iconUpdateVolume('media') :
            iconUpdateVolume('mute');
    }
    else {
        videoContent.muted = true;
        iconUpdateVolume('unmute');
    }
};

volumeMuteValue.addEventListener('click', volumeMute);
//
// update volume
function updateVolume() {
    videoContent.volume = volumeValue.value;
    if (volumeValue.value == 0) {
        iconUpdateVolume('unmute');
    } else if (videoContent.volume <= 0.5) {
        videoContent.muted = false
        iconUpdateVolume('media')
    } else {
        videoContent.muted = false
        iconUpdateVolume('mute')
    };

};
updateVolume()
volumeValue.addEventListener('input', updateVolume);

//
// change screen full window
function resizeScreen() {
    maxScreen = document.querySelector('#screen__max');
    minScreen = document.querySelector('#screen__min');
    if (document.fullscreenElement) {
        document.exitFullscreen();
        minScreen.style.display = 'none';
        maxScreen.style.display = 'initial';
    } else {
        videoPlayerContainer.requestFullscreen();
        maxScreen.style.display = 'none';
        minScreen.style.display = 'initial';
    };

    if (document.webkitFullscreenElement) {
        document.webkitExitFullscreen();
        minScreen.style.display = 'none';
        maxScreen.style.display = 'initial';
    } else {
        videoPlayerContainer.webkitRequestFullscreen();
        maxScreen.style.display = 'none';
        minScreen.style.display = 'initial';
    }
};

changeScreenButton.addEventListener('click', resizeScreen)
videoContent.addEventListener('dblclick', resizeScreen)
//
// keyboard action
function PlayerContainerListener(event) {
    if (event.key === 'p' || event.key === ' ') {
        togglePlay()
    } else if (event.key === 'm') { volumeMute() };
};

videoPlayerContainer.addEventListener('keypress', PlayerContainerListener)
//
// show controls
let timeoutValue;
function showControls() {
    videoPlayerControls.style.display = 'initial';
    videoPlayerContainer.style.cursor = 'default'
    clearTimeout(timeoutValue);
    timeoutValue = setTimeout(() => {
        videoPlayerControls.style.display = 'none';
        videoPlayerContainer.style.cursor = 'none'
        timeoutValue = undefined
    }, 5000);
};

videoPlayerContainer.addEventListener('mousemove', showControls)

// show time of video
const addingZeroFormatter = new Intl.NumberFormat(undefined, { minimumIntegerDigits: 2 });

videoContent.addEventListener('loadeddata', () => {
    videoDurationTime.textContent = timeFormat(videoContent.duration)
});
videoContent.addEventListener('timeupdate', () => {
    videoElapseTime.textContent = timeFormat(videoContent.currentTime)
});

function timeFormat(time) {
    const hours = Math.floor(time / 60 / 60)
    const minutes = Math.floor(time / 60)
    const seconds = Math.floor(time % 60)
    if (hours === 0) {
        return `${minutes}:${addingZeroFormatter.format(seconds)}`;
    } else {
        `${hours}:${addingZeroFormatter.format(minutes)}`;
    }
};


// show time on time line
videoTimeLineContainer.addEventListener('mousemove', timeLineUpdateHandel)
function timeLineUpdateHandel(event) {
    const rectParamLine = videoTimeLineContainer.getBoundingClientRect();
    const valueLine = Math.min(Math.max(0, event.x - rectParamLine.x), rectParamLine.width);
    videoTimeLineContainer.style.setProperty('--progress-time', (valueLine / rectParamLine.width));
    const foundTime = (videoContent.duration / rectParamLine.width) * valueLine
    showFoundTimeLine.textContent = timeFormat(foundTime)

    if (valueLine < (rectParamLine.width / 2)) {
        if (rectParamLine.width >= 2000) {
            videoTimeLineContainer.style.setProperty('--display-mode', 0.98);
        }
        else if (rectParamLine.width >= 1600) {
            videoTimeLineContainer.style.setProperty('--display-mode', 0.97);
        }
        else if (rectParamLine.width >= 1200) {
            videoTimeLineContainer.style.setProperty('--display-mode', 0.96);
        }
        else if (rectParamLine.width >= 700) {
            videoTimeLineContainer.style.setProperty('--display-mode', 0.94);
        }
        else if (rectParamLine.width >= 400) {
            videoTimeLineContainer.style.setProperty('--display-mode', 0.90);
        }
        else if (rectParamLine.width >= 300) {
            videoTimeLineContainer.style.setProperty('--display-mode', 0.88);
        }
        else if (rectParamLine.width >= 200) {
            videoTimeLineContainer.style.setProperty('--display-mode', 0.85);
        }
        else {
            videoTimeLineContainer.style.setProperty('--display-mode', 0.81);
        }
    } else {
        videoTimeLineContainer.style.setProperty('--display-mode', 1.01);
    }

    videoTimeLineContainer.addEventListener('click', () => {
        videoContent.currentTime = foundTime;
    })
};

// video timeline update
videoContent.addEventListener('timeupdate', () => {
    const rectParamLine = videoTimeLineContainer.getBoundingClientRect();
    const stepTime = ((rectParamLine.width / videoContent.duration) * videoContent.currentTime)
    videoTimeLineContainer.style.setProperty('--video-progress', stepTime / rectParamLine.width);
    bufferEvent(videoContent.buffered.end(videoContent.buffered.length - 1))

});

//
// show load progress bar
function bufferEvent() {
    const rectParamLine = videoTimeLineContainer.getBoundingClientRect();
    const bufferProgress = videoContent.buffered.end(videoContent.buffered.length - 1);
    const loadData = ((rectParamLine.width / videoContent.duration) * bufferProgress) / rectParamLine.width;
    videoTimeLineContainer.style.setProperty('--load-progress', loadData)
};
videoContent.addEventListener('progress', bufferEvent(videoContent.buffered.end(videoContent.buffered.length - 1)))


