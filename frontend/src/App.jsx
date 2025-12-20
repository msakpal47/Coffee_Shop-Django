import React, { useEffect, useState } from 'react'
import { BrowserRouter, Routes, Route, Link, useNavigate } from 'react-router-dom'
import './styles.css'
import logo from '../Items/logo/Ganesha.jpg'
const API_BASE = import.meta.env.VITE_API_BASE || '/api'

function Navbar() {
  return (
    <nav className="nav">
      <div className="brand"><img src={logo} alt="GANESHA" className="logo"/> GANESHA</div>
      <div className="links">
        <Link to="/">Home</Link>
        <Link to="/menu">Menu</Link>
        <Link to="/order">Order</Link>
        <Link to="/history">History</Link>
        <Link to="/add">Add items</Link>
        <a href="http://127.0.0.1:8000/coffee_login/login/" target="_blank" rel="noreferrer">Login</a>
      </div>
      <div className="contact">
        <span>+91 9892356449</span>
        <span>monishsakpl4477@gmail.com</span>
      </div>
    </nav>
  )
}

function Home() {
  return (
    <div className="hero">
      <div className="hero-content">
        <h1>GANESHA COFFEE</h1>
        <div className="subtitle">Spread Happiness</div>
        <p>
          There are many variations of passages of Lorem Ipsum available, but the
          majority have suffered alteration in some form, by injected humour, or
          randomised words.
        </p>
        <div className="cta-grid">
          <Link to="/menu" className="cta-card">
            <div className="cta-title">Explore Menu</div>
            <div className="cta-sub">Browse all items</div>
          </Link>
          <Link to="/order" className="cta-card">
            <div className="cta-title">Order</div>
            <div className="cta-sub">Review and checkout</div>
          </Link>
          <Link to="/history" className="cta-card">
            <div className="cta-title">Order History</div>
            <div className="cta-sub">Day-wise totals</div>
          </Link>
        </div>
      </div>
    </div>
  )
}

function Menu() {
  const [items, setItems] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState(null)
  const navigate = useNavigate()

  useEffect(() => {
    const run = async () => {
      setLoading(true)
      try {
        const res = await fetch(`${API_BASE}/coffee_Shop/api/menu/`)
        if (!res.ok) {
           throw new Error(`HTTP error! status: ${res.status}`)
        }
        const data = await res.json()
        setItems(data.items || [])
      } catch (err) {
        console.error("Failed to fetch menu:", err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    run()
  }, [])
  return (
    <div className="page">
      <h2 className="title">Menu</h2>
      {loading && <p>Loading...</p>}
      {error && <p className="error">Error loading menu: {error}</p>}
      <div className="grid">
        {items.map(i => (
          <div key={i.id} className="card">
            {i.image_url && <img src={i.image_url} alt={i.name} />}
            <div className="name">{i.name}</div>
            <div className="desc">{i.description}</div>
            <div className="price">₹{Number(i.price).toFixed(2)}</div>
            <button className="btn" onClick={async()=>{
              await fetch(`${API_BASE}/coffee_Shop/api/menu/add_to_order/${i.id}/`,{method:'POST'})
              navigate('/order')
            }}>Add</button>
          </div>
        ))}
      </div>
    </div>
  )
}

function Order() {
  const [order, setOrder] = useState({ items: [], total: 0 })
  const [customerName, setCustomerName] = useState('')
  const [customerEmail, setCustomerEmail] = useState('')
  const [customerPhone, setCustomerPhone] = useState('')

  const load = async () => {
    const r = await fetch(`${API_BASE}/coffee_Shop/api/order/`)
    const d = await r.json()
    setOrder(d)
  }
  useEffect(() => { load() }, [])

  const handleConfirm = async () => {
    if (!customerName || !customerPhone) {
      alert("Please enter Name and Phone number.")
      return
    }
    const res = await fetch(`${API_BASE}/coffee_Shop/api/order/confirm/`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        name: customerName,
        email: customerEmail,
        phone: customerPhone
      })
    });
    if (res.ok) {
      alert("Order confirmed!")
      setCustomerName('')
      setCustomerEmail('')
      setCustomerPhone('')
      await load()
    } else {
      alert("Failed to confirm order")
    }
  }

  return (
    <div className="page">
      <h2 className="title">Your Order</h2>
      <table className="table">
        <thead>
          <tr>
            <th>Image</th><th>Items</th><th>Price</th><th>Quantity</th><th>Total</th><th></th>
          </tr>
        </thead>
        <tbody>
          {order.items.map(i => (
            <tr key={i.id}>
              <td>{i.image_url && <img src={i.image_url} alt="" className="thumb"/>}</td>
              <td>{i.name}</td>
              <td>₹{Number(i.price).toFixed(2)}</td>
              <td>{i.quantity}</td>
              <td>₹{Number(i.subtotal).toFixed(2)}</td>
              <td>
                <button className="icon" title="remove one" onClick={async()=>{await fetch(`${API_BASE}/coffee_Shop/api/order/delete/${i.id}/`,{method:'POST'}); load()}}>–</button>
                <button className="icon" title="remove all" onClick={async()=>{await fetch(`${API_BASE}/coffee_Shop/api/order/remove/${i.id}/`,{method:'POST'}); load()}}>×</button>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
      <div className="total">₹{Number(order.total).toFixed(2)}</div>
      
      {order.items.length > 0 && (
        <div className="customer-form" style={{maxWidth: 400, margin: '20px auto', display:'flex', flexDirection:'column', gap: 10}}>
          <h3>Customer Details</h3>
          <input placeholder="Name" value={customerName} onChange={e=>setCustomerName(e.target.value)} style={{padding:8}} />
          <input placeholder="Email" value={customerEmail} onChange={e=>setCustomerEmail(e.target.value)} style={{padding:8}} />
          <input placeholder="Phone" value={customerPhone} onChange={e=>setCustomerPhone(e.target.value)} style={{padding:8}} />
        </div>
      )}

      <div style={{display:'flex',gap:12, justifyContent:'center'}}>
        <Link className="link" to="/menu">← Back to Menu</Link>
        {order.items.length > 0 && (
          <button className="btn success" onClick={handleConfirm}>✓ Confirm & Order</button>
        )}
      </div>
    </div>
  )
}

function AddItem() {
  const [name, setName] = useState('')
  const [description, setDescription] = useState('')
  const [price, setPrice] = useState('')
  const [image, setImage] = useState(null)
  const [msg, setMsg] = useState('')
  const submit = async e => {
    e.preventDefault()
    const form = new FormData()
    form.append('name', name)
    form.append('description', description)
    form.append('price', price)
    if (image) form.append('image', image)
    const res = await fetch('/api/coffee_Shop/api/menu/', { method: 'POST', body: form })
    if (res.ok) setMsg('Item added')
    else setMsg('Failed')
  }
  return (
    <div className="page">
      <h2 className="title">Add Item</h2>
      <form onSubmit={submit} className="form">
        <input placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
        <textarea placeholder="Description" value={description} onChange={e=>setDescription(e.target.value)} />
        <input type="number" step="0.01" placeholder="Price" value={price} onChange={e=>setPrice(e.target.value)} />
        <input type="file" accept="image/*" onChange={e=>setImage(e.target.files[0]||null)} />
        <button className="btn" type="submit">Add</button>
      </form>
      {msg && <p>{msg}</p>}
    </div>
  )
}

function History() {
  const [date, setDate] = useState(() => {
    const d = new Date()
    const y = d.getFullYear()
    const m = String(d.getMonth() + 1).padStart(2, '0')
    const day = String(d.getDate()).padStart(2, '0')
    return `${y}-${m}-${day}`
  })
  const [orders, setOrders] = useState([])
  const [totalForDate, setTotalForDate] = useState(0)
  const [dailyTotals, setDailyTotals] = useState([])
  const [loading, setLoading] = useState(false)

  const load = async (dstr) => {
    setLoading(true)
    try {
      const r = await fetch(`${API_BASE}/coffee_Shop/api/orders/history/?date=${encodeURIComponent(dstr)}`)
      const data = await r.json()
      setOrders(data.orders || [])
      setTotalForDate(data.total_for_date || 0)
      setDailyTotals(data.daily_totals || [])
    } finally {
      setLoading(false)
    }
  }
  useEffect(() => { load(date) }, [date])

  return (
    <div className="page">
      <h2 className="title">Order History</h2>
      <div style={{display:'flex', gap:12, alignItems:'center', justifyContent:'center', marginBottom:12}}>
        <label>Select day:</label>
        <input type="date" value={date} onChange={e=>setDate(e.target.value)} />
      </div>
      {loading && <p>Loading...</p>}
      <table className="table">
        <thead>
          <tr>
            <th>Order ID</th><th>Time</th><th>Customer</th><th>Total</th><th>Items</th>
          </tr>
        </thead>
        <tbody>
          {orders.map(o => (
            <tr key={o.order_id}>
              <td>{o.order_id}</td>
              <td>{o.time}</td>
              <td>{o.customer_name}</td>
              <td>₹{Number(o.total_price).toFixed(2)}</td>
              <td>{o.items}</td>
            </tr>
          ))}
          {orders.length === 0 && !loading && (
            <tr><td colSpan="5" style={{textAlign:'center'}}>No orders for selected day</td></tr>
          )}
        </tbody>
      </table>
      <div className="total">End of Day Total: ₹{Number(totalForDate).toFixed(2)}</div>

      <h3 style={{marginTop:24}}>Daily Totals</h3>
      <table className="table">
        <thead>
          <tr><th>Date</th><th>Total</th></tr>
        </thead>
        <tbody>
          {dailyTotals.map(d => (
            <tr key={d.date}>
              <td>{d.date}</td>
              <td>₹{Number(d.total).toFixed(2)}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  )
}

export default function App() {
  return (
    <BrowserRouter>
      <Navbar />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/menu" element={<Menu />} />
        <Route path="/order" element={<Order />} />
        <Route path="/history" element={<History />} />
        <Route path="/add" element={<AddItem />} />
      </Routes>
    </BrowserRouter>
  )
}
