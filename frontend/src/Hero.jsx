export default function Hero() {


	const styles = {
	hero: {
		position: 'relative',
		height: '100vh',
		overflow: 'hidden',
	},
	video: {
		position: 'absolute',
		top: 0,
		left: 0,
		width: '100%',
		height: '100%',
		objectFit: 'cover',
		zIndex: 1,
	},
	overlay: {
		position: 'relative',
		zIndex: 2,
		color: 'white',
		textAlign: 'center',
		top: '50%',
		transform: 'translateY(-50%)',
	},
	title: {
		fontSize: '3rem',
		fontWeight: 'bold',
		marginBottom: '1rem',
	},
	subtitle: {
		fontSize: '1.5rem',
	},
	};

	return (
		<>
			<section style={styles.hero}>
			<video
				autoPlay
				loop
				muted
				playsInline
				style={styles.video}
			>
				<source src="https://storage.googleapis.com/keiser-web/video/jellyfish2.mov" type="video/mp4" />
				Your browser does not support the video tag.
			</video>

			<h1 style={{ color: "#ff99fdff", fontWeight: "900" }}>
				"I am Iron Man!"
			</h1>
			</section>
		</>
	);
}