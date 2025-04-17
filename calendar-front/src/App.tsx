import Navbar from './components/Navbar'
import HomePage from './pages/HomePage'
import './App.css'

function App() {
  return (
    <>
      <Navbar />
      <main className="pt-16">
        <HomePage />
      </main>
    </>
  )
}

export default App
