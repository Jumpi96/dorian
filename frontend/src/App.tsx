import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom'
import Home from './components/Home'
import WardrobePage from './pages/WardrobePage'

function App() {
  return (
    <Router>
      <div className="min-h-screen bg-gray-50">
        {/* Navigation */}
        <nav className="bg-white shadow-sm">
          <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
            <div className="flex justify-between h-16">
              <div className="flex space-x-8">
                <Link to="/" className="inline-flex items-center px-1 pt-1 text-gray-900 hover:text-gray-600">
                  Home
                </Link>
                <Link to="/wardrobe" className="inline-flex items-center px-1 pt-1 text-gray-900 hover:text-gray-600">
                  Wardrobe
                </Link>
              </div>
            </div>
          </div>
        </nav>

        {/* Routes */}
        <main className="py-10">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/wardrobe" element={<WardrobePage />} />
          </Routes>
        </main>
      </div>
    </Router>
  )
}

export default App
