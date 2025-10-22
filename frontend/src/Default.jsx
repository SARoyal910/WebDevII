function Default() {

	return (
		<>
		<div style={{ backgroundColor: "blue" }}>
			<a href="https://vite.dev" target="_blank">
			<img src={viteLogo} className="logo react" alt="React logo" />
			</a>
			<img src="https://storage.googleapis.com/keiser-web/img/trapezoid.png" className="logo" alt="Vite logo" />
			<a href="https://react.dev" target="_blank">
			<img src={reactLogo} className="logo react" alt="React logo" />
			</a>
		</div>
		<h1>Vite + React</h1>
		<div className="card">
			<button onClick={() => setCount((count) => count + 1)}>
			count is {count}
			</button>
			<p>
			Edit <code>src/App.jsx</code> and save to test HMR
			</p>
		</div>

		<div className="card">
			<button onClick={fastapiExample}>
			Call FastAPI and display HTML
			</button>
			{/* Conditional rendering: only show the HTML if it exists in the state */}
			{htmlContent && (
			<div dangerouslySetInnerHTML={{ __html: JSON.stringify(htmlContent) }} />
			)}
		</div>

		<button onClick={redisTestGet}>Get Test</button>


		<button onClick={redisTestSet}>Set Test</button>

		<div>
			{redisContent && (
			<div dangerouslySetInnerHTML={{ __html: JSON.stringify(redisContent) }} />
			)}
		</div>

		<form onSubmit="">

		</form>

		<p className="read-the-docs">
			Click on the Vite and React logos to learn more
		</p>
		</>
	)
}

export default Default