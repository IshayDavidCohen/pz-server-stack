import './VideoBackground.css'

function VideoBackground() {
  return (
    <div className="video-background-container">
      <video
        className="video-background"
        autoPlay
        loop
        muted
        playsInline
      >
        <source src="/safehouse-video.mp4" type="video/mp4" />
      </video>
    </div>
  )
}

export default VideoBackground

