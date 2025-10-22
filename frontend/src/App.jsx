import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Hero from './Hero.jsx'
import axios from 'axios'

function App() {
  const [count, setCount] = useState(0)

  // Login States
  const [email, setEmail] = useState("")
  const [password, setPassword] = useState("")

  // State to hold the HTML content from the FastAPI backend
  const [htmlContent, setHtmlContent] = useState(null)
  const [redisContent, setRedisContent] = useState(null)

  const fastapiExample = async () => {
    console.log("We are trying to reach out to FastAPI")
    try {
      const response = await axios.get("http://localhost:8000/react-demo")
      console.log(JSON.stringify(response.data));
      // Store the received HTML string in the state
      setHtmlContent(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
      setHtmlContent("<p style='color:red;'>Failed to fetch data.</p>");
    }
  }

  const redisTestSet = async () => {
    console.log("We are trying to reach out to FastAPI")
    try {
      const response = await axios.get("http://localhost:8000/redis-set-test")
      console.log(JSON.stringify(response.data));
      // Store the received HTML string in the state
      setRedisContent(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
      setRedisContent("<p style='color:red;'>Failed to fetch data.</p>");
    }
  }

  const redisTestGet = async () => {
    console.log("We are trying to reach out to FastAPI")
    try {
      const response = await axios.get("http://localhost:8000/redis-get-test")
      console.log(JSON.stringify(response.data));
      // Store the received HTML string in the state
      setRedisContent(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
      setRedisContent("<p style='color:red;'>Failed to fetch data.</p>");
    }
  }

  return (
    <>
      <Hero />
    </>
  )
}

export default App