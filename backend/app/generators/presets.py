import json
from typing import Dict, Any, List

def get_hotel_booking_files(title: str = "Grand Horizon Hotel & Resort") -> Dict[str, str]:
    """Generates complete source code files for a luxury hotel booking web application."""
    
    html_preview = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-50 text-slate-800 font-sans antialiased">
  <!-- Top Banner / Navbar -->
  <header class="bg-slate-900 text-white sticky top-0 z-50 shadow-md">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between">
      <div class="flex items-center gap-2">
        <i class="fa-solid fa-hotel text-teal-400 text-xl"></i>
        <span class="font-bold text-lg tracking-wide">{title}</span>
      </div>
      <div class="flex items-center gap-4 text-sm font-medium">
        <span class="hidden sm:inline text-slate-300">24/7 Concierge: +1 (800) 555-0199</span>
        <button onclick="document.getElementById('booking-section').scrollIntoView({{behavior: 'smooth'}})" class="bg-teal-600 hover:bg-teal-500 text-white px-4 py-2 rounded-lg transition-colors">
          Book Now
        </button>
      </div>
    </div>
  </header>

  <!-- Hero Section -->
  <section class="relative bg-slate-900 text-white py-20 px-4 text-center overflow-hidden">
    <div class="absolute inset-0 opacity-40 bg-cover bg-center" style="background-image: url('https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1600&q=80')"></div>
    <div class="relative max-w-3xl mx-auto space-y-4">
      <span class="bg-teal-500/20 text-teal-300 text-xs px-3 py-1 rounded-full uppercase tracking-wider font-semibold border border-teal-500/30">Luxury Accommodations</span>
      <h1 class="text-3xl sm:text-5xl font-extrabold tracking-tight">Experience Unrivaled Comfort & Elegance</h1>
      <p class="text-slate-200 text-sm sm:text-base">Handcrafted suites with panoramic ocean views, private spas, and world-class dining.</p>
    </div>
  </section>

  <!-- Search & Filter Bar -->
  <div id="booking-section" class="max-w-6xl mx-auto -mt-8 px-4 relative z-20">
    <div class="bg-white rounded-2xl shadow-xl p-4 sm:p-6 border border-slate-100 flex flex-col md:flex-row gap-4 items-center justify-between">
      <div class="w-full md:w-1/4">
        <label class="block text-xs font-semibold text-slate-500 uppercase">Room Category</label>
        <select id="type-filter" onchange="filterRooms()" class="mt-1 w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm font-medium focus:ring-2 focus:ring-teal-500">
          <option value="all">All Room Types</option>
          <option value="Deluxe">Deluxe King</option>
          <option value="Suite">Presidential Suite</option>
          <option value="Ocean View">Oceanfront Villa</option>
        </select>
      </div>
      <div class="w-full md:w-1/4">
        <label class="block text-xs font-semibold text-slate-500 uppercase">Check-in Date</label>
        <input type="date" id="checkin-date" value="2026-11-15" class="mt-1 w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm font-medium focus:ring-2 focus:ring-teal-500">
      </div>
      <div class="w-full md:w-1/4">
        <label class="block text-xs font-semibold text-slate-500 uppercase">Nights</label>
        <input type="number" id="nights-count" min="1" max="30" value="2" onchange="updatePriceEstimates()" class="mt-1 w-full bg-slate-50 border border-slate-200 rounded-lg p-2.5 text-sm font-medium focus:ring-2 focus:ring-teal-500">
      </div>
      <div class="w-full md:w-1/4 pt-4 md:pt-0">
        <button onclick="filterRooms()" class="w-full bg-teal-600 hover:bg-teal-500 text-white font-semibold py-2.5 px-4 rounded-lg shadow-md transition-colors flex items-center justify-center gap-2">
          <i class="fa-solid fa-magnifying-glass"></i> Find Rooms
        </button>
      </div>
    </div>
  </div>

  <!-- Rooms Grid -->
  <main class="max-w-6xl mx-auto px-4 py-12">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h2 class="text-2xl font-bold text-slate-900">Featured Suites & Villas</h2>
        <p class="text-sm text-slate-500">Live inventory synced with central booking engine</p>
      </div>
      <span id="room-count-badge" class="bg-teal-100 text-teal-800 text-xs font-semibold px-3 py-1 rounded-full">Showing 3 suites</span>
    </div>

    <div id="rooms-grid" class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <!-- Injected by JavaScript -->
    </div>
  </main>

  <!-- Interactive Booking Modal -->
  <div id="booking-modal" class="fixed inset-0 z-50 hidden bg-black/60 backdrop-blur-sm flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl max-w-lg w-full p-6 shadow-2xl space-y-4">
      <div class="flex items-center justify-between border-b pb-3">
        <h3 id="modal-title" class="text-lg font-bold text-slate-900">Confirm Reservation</h3>
        <button onclick="closeModal()" class="text-slate-400 hover:text-slate-600"><i class="fa-solid fa-xmark text-lg"></i></button>
      </div>
      <div class="space-y-3 text-sm">
        <div class="flex justify-between text-slate-600"><span>Price per Night:</span> <strong id="modal-rate" class="text-slate-900">$0</strong></div>
        <div class="flex justify-between text-slate-600"><span>Duration:</span> <strong id="modal-nights" class="text-slate-900">0 nights</strong></div>
        <div class="flex justify-between text-slate-600"><span>Taxes & Resort Fee (12%):</span> <strong id="modal-taxes" class="text-slate-900">$0</strong></div>
        <div class="flex justify-between text-base font-bold text-teal-700 border-t pt-2"><span>Total Amount:</span> <span id="modal-total">$0</span></div>

        <form id="reservation-form" onsubmit="handleReserve(event)" class="space-y-3 pt-2">
          <div>
            <label class="block text-xs font-medium text-slate-700">Guest Full Name</label>
            <input type="text" required placeholder="John Doe" class="mt-1 w-full border border-slate-300 rounded-lg p-2 text-sm focus:ring-2 focus:ring-teal-500">
          </div>
          <div>
            <label class="block text-xs font-medium text-slate-700">Guest Email Address</label>
            <input type="email" required placeholder="john@example.com" class="mt-1 w-full border border-slate-300 rounded-lg p-2 text-sm focus:ring-2 focus:ring-teal-500">
          </div>
          <button type="submit" class="w-full bg-teal-600 hover:bg-teal-500 text-white font-semibold py-2.5 rounded-lg shadow transition-colors">
            Confirm & Pay at Check-in
          </button>
        </form>
      </div>
    </div>
  </div>

  <!-- Success Notification Dialog -->
  <div id="success-toast" class="fixed bottom-6 right-6 z-50 hidden bg-emerald-600 text-white px-5 py-3 rounded-xl shadow-2xl flex items-center gap-3">
    <i class="fa-solid fa-circle-check text-xl"></i>
    <div>
      <div class="font-bold text-sm">Reservation Confirmed!</div>
      <div class="text-xs text-emerald-100">Confirmation receipt dispatched to guest email.</div>
    </div>
  </div>

  <script>
    const rooms = [
      {{
        id: 1,
        title: "Oceanfront Luxury Villa",
        type: "Ocean View",
        price: 450,
        rating: 4.9,
        reviews: 128,
        image: "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=600&q=80",
        amenities: ["Private Infinity Pool", "Oceanfront Terrace", "King Bed", "Jacuzzi", "Free Breakfast"]
      }},
      {{
        id: 2,
        title: "Presidential Sky Suite",
        type: "Suite",
        price: 680,
        rating: 5.0,
        reviews: 94,
        image: "https://images.unsplash.com/photo-1631049307264-da0ec9d70304?auto=format&fit=crop&w=600&q=80",
        amenities: ["Top Floor Penthouse", "Butler Service", "Sauna", "Wine Cellar", "Airport Shuttle"]
      }},
      {{
        id: 3,
        title: "Deluxe Garden King",
        type: "Deluxe",
        price: 290,
        rating: 4.8,
        reviews: 215,
        image: "https://images.unsplash.com/photo-1618773928121-c32242e63f39?auto=format&fit=crop&w=600&q=80",
        amenities: ["Botanical Garden View", "King Featherbed", "Espresso Bar", "High-speed WiFi"]
      }}
    ];

    let selectedRoom = null;

    function renderRooms(items) {{
      const grid = document.getElementById('rooms-grid');
      grid.innerHTML = items.map(room => `
        <div class="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm hover:shadow-lg transition-all flex flex-col">
          <div class="relative h-48 overflow-hidden">
            <img src="${{room.image}}" alt="${{room.title}}" class="w-full h-full object-cover hover:scale-105 transition-transform duration-300">
            <span class="absolute top-3 right-3 bg-white/95 backdrop-blur-sm text-slate-900 text-xs font-bold px-2.5 py-1 rounded-full shadow">
              <i class="fa-solid fa-star text-amber-400"></i> ${{room.rating}} (${{room.reviews}})
            </span>
          </div>
          <div class="p-5 flex-1 flex flex-col justify-between space-y-4">
            <div>
              <span class="text-xs font-bold text-teal-600 uppercase tracking-wider">${{room.type}}</span>
              <h3 class="text-lg font-bold text-slate-900 mt-0.5">${{room.title}}</h3>
              <div class="flex flex-wrap gap-1.5 mt-3">
                ${{room.amenities.map(a => `<span class="bg-slate-100 text-slate-600 text-[11px] px-2 py-0.5 rounded-md">${{a}}</span>`).join('')}}
              </div>
            </div>
            <div class="pt-4 border-t border-slate-100 flex items-center justify-between">
              <div>
                <span class="text-2xl font-black text-slate-900">$${{room.price}}</span>
                <span class="text-xs text-slate-400">/ night</span>
              </div>
              <button onclick="openBookingModal(${{room.id}})" class="bg-teal-600 hover:bg-teal-700 text-white font-medium text-xs px-4 py-2 rounded-lg transition-colors">
                Reserve Suite
              </button>
            </div>
          </div>
        </div>
      `).join('');
      document.getElementById('room-count-badge').textContent = `Showing ${{items.length}} suite${{items.length === 1 ? '' : 's'}}`;
    }}

    function filterRooms() {{
      const type = document.getElementById('type-filter').value;
      const filtered = type === 'all' ? rooms : rooms.filter(r => r.type === type);
      renderRooms(filtered);
    }}

    function openBookingModal(roomId) {{
      selectedRoom = rooms.find(r => r.id === roomId);
      if (!selectedRoom) return;

      const nights = parseInt(document.getElementById('nights-count').value) || 2;
      const subtotal = selectedRoom.price * nights;
      const taxes = Math.round(subtotal * 0.12);
      const total = subtotal + taxes;

      document.getElementById('modal-title').textContent = `Book: ${{selectedRoom.title}}`;
      document.getElementById('modal-rate').textContent = `$${{selectedRoom.price}}`;
      document.getElementById('modal-nights').textContent = `${{nights}} night${{nights > 1 ? 's' : ''}}`;
      document.getElementById('modal-taxes').textContent = `$${{taxes}}`;
      document.getElementById('modal-total').textContent = `$${{total}}`;
      document.getElementById('booking-modal').classList.remove('hidden');
    }}

    function closeModal() {{
      document.getElementById('booking-modal').classList.add('hidden');
    }}

    function handleReserve(e) {{
      e.preventDefault();
      closeModal();
      const toast = document.getElementById('success-toast');
      toast.classList.remove('hidden');
      setTimeout(() => toast.classList.add('hidden'), 4000);
    }}

    // Initial render
    renderRooms(rooms);
  </script>
</body>
</html>"""

    return {
        "index.html": html_preview,
        "README.md": f"# {title}\n\nGenerated by BuildPilot AI.\n\n## Features\n- Live room inventory catalog\n- Dynamic date & night calculator\n- Interactive booking modal with price breakdowns\n- Responsive Tailwind CSS styling"
    }

def get_ecommerce_files(title: str = "Nexus Commerce & Admin") -> Dict[str, str]:
    """Generates complete source code files for an E-commerce store with integrated Admin dashboard."""
    html_preview = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-gray-50 text-gray-900 font-sans antialiased">
  <!-- Header -->
  <header class="bg-white border-b border-gray-200 sticky top-0 z-40">
    <div class="max-w-7xl mx-auto px-4 sm:px-6 h-16 flex items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <div class="w-8 h-8 rounded-lg bg-indigo-600 flex items-center justify-center text-white font-black text-sm">N</div>
        <span class="font-extrabold text-lg tracking-tight text-gray-900">{title}</span>
      </div>

      <div class="flex-1 max-w-md hidden sm:block">
        <div class="relative">
          <i class="fa-solid fa-search absolute left-3 top-3 text-gray-400 text-sm"></i>
          <input type="text" id="search-input" onkeyup="handleSearch()" placeholder="Search gadgets, audio, wearables..." class="w-full bg-gray-100 pl-9 pr-4 py-2 rounded-xl text-sm border-0 focus:ring-2 focus:ring-indigo-600 focus:bg-white transition-all">
        </div>
      </div>

      <div class="flex items-center gap-3">
        <!-- Toggle Admin Mode -->
        <button onclick="toggleAdminView()" id="admin-toggle-btn" class="text-xs font-semibold px-3 py-1.5 rounded-lg border border-indigo-200 text-indigo-700 bg-indigo-50 hover:bg-indigo-100 transition-colors flex items-center gap-1.5">
          <i class="fa-solid fa-chart-line"></i> <span id="admin-btn-text">Admin Dashboard</span>
        </button>

        <!-- Cart Button -->
        <button onclick="openCart()" class="relative p-2 rounded-xl text-gray-700 hover:bg-gray-100 transition-colors">
          <i class="fa-solid fa-bag-shopping text-xl"></i>
          <span id="cart-badge" class="absolute -top-1 -right-1 bg-indigo-600 text-white text-[10px] font-bold w-5 h-5 rounded-full flex items-center justify-center">0</span>
        </button>
      </div>
    </div>
  </header>

  <!-- Store Front View -->
  <div id="store-view">
    <main class="max-w-7xl mx-auto px-4 sm:px-6 py-8">
      <!-- Category Tabs -->
      <div class="flex gap-2 overflow-x-auto pb-4 mb-6">
        <button onclick="filterCategory('All')" class="category-btn active px-4 py-2 rounded-xl text-xs font-bold bg-indigo-600 text-white shadow-sm transition-colors">All Products</button>
        <button onclick="filterCategory('Audio')" class="category-btn px-4 py-2 rounded-xl text-xs font-semibold bg-white border border-gray-200 text-gray-700 hover:bg-gray-100 transition-colors">Audio</button>
        <button onclick="filterCategory('Wearables')" class="category-btn px-4 py-2 rounded-xl text-xs font-semibold bg-white border border-gray-200 text-gray-700 hover:bg-gray-100 transition-colors">Wearables</button>
        <button onclick="filterCategory('Accessories')" class="category-btn px-4 py-2 rounded-xl text-xs font-semibold bg-white border border-gray-200 text-gray-700 hover:bg-gray-100 transition-colors">Accessories</button>
      </div>

      <!-- Products Grid -->
      <div id="products-grid" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6"></div>
    </main>
  </div>

  <!-- Admin Dashboard View -->
  <div id="admin-view" class="hidden max-w-7xl mx-auto px-4 sm:px-6 py-8 space-y-6">
    <div class="flex items-center justify-between border-b pb-4">
      <div>
        <h2 class="text-2xl font-bold text-gray-900">Admin Control Center</h2>
        <p class="text-xs text-gray-500">Real-time revenue metrics, inventory control, and order fulfillment</p>
      </div>
      <button onclick="toggleAdminView()" class="text-xs font-medium text-gray-500 hover:text-gray-900">← Return to Storefront</button>
    </div>

    <!-- Stat Metric Cards -->
    <div class="grid grid-cols-1 sm:grid-cols-3 gap-6">
      <div class="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm">
        <div class="text-xs font-semibold text-gray-400 uppercase">Gross Revenue</div>
        <div class="text-3xl font-extrabold text-indigo-600 mt-1">$28,450.00</div>
        <div class="text-xs text-emerald-600 font-medium mt-1"><i class="fa-solid fa-arrow-trend-up"></i> +14.2% vs last month</div>
      </div>
      <div class="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm">
        <div class="text-xs font-semibold text-gray-400 uppercase">Total Orders</div>
        <div class="text-3xl font-extrabold text-gray-900 mt-1">1,429</div>
        <div class="text-xs text-emerald-600 font-medium mt-1"><i class="fa-solid fa-check"></i> 99.4% Fulfillment rate</div>
      </div>
      <div class="bg-white p-5 rounded-2xl border border-gray-200 shadow-sm">
        <div class="text-xs font-semibold text-gray-400 uppercase">Active Inventory</div>
        <div class="text-3xl font-extrabold text-emerald-600 mt-1">428 units</div>
        <div class="text-xs text-gray-500 font-medium mt-1">Across 4 core product categories</div>
      </div>
    </div>

    <!-- Inventory Stock Table -->
    <div class="bg-white rounded-2xl border border-gray-200 shadow-sm overflow-hidden">
      <div class="p-4 border-b border-gray-100 flex justify-between items-center">
        <h3 class="font-bold text-sm text-gray-900">Live Inventory Manager</h3>
        <span class="text-xs text-gray-400">Synced with MongoDB</span>
      </div>
      <table class="w-full text-left text-xs sm:text-sm">
        <thead class="bg-gray-50 text-gray-500 uppercase text-[11px]">
          <tr>
            <th class="p-3">Product Name</th>
            <th class="p-3">Category</th>
            <th class="p-3">Unit Price</th>
            <th class="p-3">In Stock</th>
            <th class="p-3">Action</th>
          </tr>
        </thead>
        <tbody id="inventory-table-body" class="divide-y divide-gray-100"></tbody>
      </table>
    </div>
  </div>

  <!-- Cart Slide-Over Drawer -->
  <div id="cart-drawer" class="fixed inset-0 z-50 hidden bg-black/50 backdrop-blur-xs flex justify-end">
    <div class="bg-white w-full max-w-md h-full flex flex-col shadow-2xl p-6">
      <div class="flex items-center justify-between border-b pb-4">
        <h3 class="font-bold text-lg text-gray-900">Shopping Cart (<span id="cart-item-count">0</span>)</h3>
        <button onclick="closeCart()" class="text-gray-400 hover:text-gray-600"><i class="fa-solid fa-xmark text-xl"></i></button>
      </div>

      <div id="cart-items" class="flex-1 overflow-y-auto py-4 space-y-3">
        <div class="text-center text-gray-400 py-12 text-sm">Your cart is empty</div>
      </div>

      <div class="border-t pt-4 space-y-3">
        <div class="flex justify-between font-bold text-base text-gray-900">
          <span>Subtotal:</span>
          <span id="cart-subtotal">$0.00</span>
        </div>
        <button onclick="checkout()" class="w-full bg-indigo-600 hover:bg-indigo-500 text-white font-bold py-3 rounded-xl shadow-md transition-colors">
          Proceed to Checkout
        </button>
      </div>
    </div>
  </div>

  <script>
    const products = [
      {{ id: 1, name: "Spatial Pro Noise-Cancelling Headphones", category: "Audio", price: 349, rating: 4.9, stock: 45, image: "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?auto=format&fit=crop&w=500&q=80" }},
      {{ id: 2, name: "UltraFit Titanium Smart Watch", category: "Wearables", price: 279, rating: 4.8, stock: 62, image: "https://images.unsplash.com/photo-1523275335684-37898b6baf30?auto=format&fit=crop&w=500&q=80" }},
      {{ id: 3, name: "Minimalist MagSafe Charging Stand", category: "Accessories", price: 89, rating: 4.7, stock: 110, image: "https://images.unsplash.com/photo-1583394838336-acd977736f90?auto=format&fit=crop&w=500&q=80" }},
      {{ id: 4, name: "Studio Earbuds with ANC & Wireless Case", category: "Audio", price: 199, rating: 4.8, stock: 80, image: "https://images.unsplash.com/photo-1590658268037-6bf12165a8df?auto=format&fit=crop&w=500&q=80" }}
    ];

    let cart = [];
    let currentCategory = 'All';

    function renderProducts(items) {{
      const grid = document.getElementById('products-grid');
      grid.innerHTML = items.map(p => `
        <div class="bg-white rounded-2xl border border-gray-200 overflow-hidden shadow-sm hover:shadow-md transition-all flex flex-col">
          <div class="h-48 bg-gray-100 overflow-hidden">
            <img src="${{p.image}}" alt="${{p.name}}" class="w-full h-full object-cover hover:scale-105 transition-transform duration-300">
          </div>
          <div class="p-4 flex-1 flex flex-col justify-between space-y-3">
            <div>
              <span class="text-[10px] font-bold text-indigo-600 uppercase tracking-wider">${{p.category}}</span>
              <h4 class="font-bold text-sm text-gray-900 mt-0.5 line-clamp-1">${{p.name}}</h4>
              <div class="text-xs text-amber-500 mt-1"><i class="fa-solid fa-star"></i> ${{p.rating}}</div>
            </div>
            <div class="flex items-center justify-between pt-2 border-t border-gray-100">
              <span class="text-lg font-black text-gray-900">$${{p.price}}</span>
              <button onclick="addToCart(${{p.id}})" class="bg-indigo-600 hover:bg-indigo-700 text-white text-xs font-semibold px-3 py-1.5 rounded-lg transition-colors">
                + Add
              </button>
            </div>
          </div>
        </div>
      `).join('');
    }}

    function filterCategory(cat) {{
      currentCategory = cat;
      const filtered = cat === 'All' ? products : products.filter(p => p.category === cat);
      renderProducts(filtered);
    }}

    function handleSearch() {{
      const query = document.getElementById('search-input').value.toLowerCase();
      const filtered = products.filter(p => p.name.toLowerCase().includes(query) || p.category.toLowerCase().includes(query));
      renderProducts(filtered);
    }}

    function addToCart(id) {{
      const item = products.find(p => p.id === id);
      const existing = cart.find(c => c.id === id);
      if (existing) {{
        existing.qty += 1;
      }} else {{
        cart.push({{ ...item, qty: 1 }});
      }}
      updateCartUI();
    }}

    function updateCartUI() {{
      const totalQty = cart.reduce((sum, i) => sum + i.qty, 0);
      document.getElementById('cart-badge').textContent = totalQty;
      document.getElementById('cart-item-count').textContent = totalQty;

      const itemsContainer = document.getElementById('cart-items');
      if (cart.length === 0) {{
        itemsContainer.innerHTML = '<div class="text-center text-gray-400 py-12 text-sm">Your cart is empty</div>';
        document.getElementById('cart-subtotal').textContent = '$0.00';
        return;
      }}

      let subtotal = 0;
      itemsContainer.innerHTML = cart.map(item => {{
        subtotal += item.price * item.qty;
        return `
          <div class="flex items-center justify-between p-2 rounded-xl bg-gray-50 border border-gray-100">
            <div class="flex items-center gap-3">
              <img src="${{item.image}}" class="w-10 h-10 object-cover rounded-lg">
              <div>
                <div class="text-xs font-bold text-gray-900 line-clamp-1">${{item.name}}</div>
                <div class="text-xs text-gray-500">$${{item.price}} x ${{item.qty}}</div>
              </div>
            </div>
            <div class="font-bold text-sm text-gray-900">$${{item.price * item.qty}}</div>
          </div>
        `;
      }}).join('');

      document.getElementById('cart-subtotal').textContent = `$${{subtotal.toFixed(2)}}`;
    }}

    function openCart() {{ document.getElementById('cart-drawer').classList.remove('hidden'); }}
    function closeCart() {{ document.getElementById('cart-drawer').classList.add('hidden'); }}

    function checkout() {{
      if (cart.length === 0) return;
      alert('Order placed successfully! Total: ' + document.getElementById('cart-subtotal').textContent);
      cart = [];
      updateCartUI();
      closeCart();
    }}

    function toggleAdminView() {{
      const store = document.getElementById('store-view');
      const admin = document.getElementById('admin-view');
      const btnText = document.getElementById('admin-btn-text');
      if (admin.classList.contains('hidden')) {{
        admin.classList.remove('hidden');
        store.classList.add('hidden');
        btnText.textContent = 'Storefront View';
        renderInventoryTable();
      }} else {{
        admin.classList.add('hidden');
        store.classList.remove('hidden');
        btnText.textContent = 'Admin Dashboard';
      }}
    }}

    function renderInventoryTable() {{
      const tbody = document.getElementById('inventory-table-body');
      tbody.innerHTML = products.map(p => `
        <tr class="hover:bg-gray-50">
          <td class="p-3 font-semibold text-gray-900">${{p.name}}</td>
          <td class="p-3 text-gray-500">${{p.category}}</td>
          <td class="p-3 font-mono font-medium">$${{p.price}}</td>
          <td class="p-3"><span class="px-2 py-0.5 rounded-full text-xs ${{p.stock > 50 ? 'bg-emerald-100 text-emerald-800' : 'bg-amber-100 text-amber-800'}}">${{p.stock}} units</span></td>
          <td class="p-3"><button onclick="alert('Restocked ${{p.name}}')" class="text-xs text-indigo-600 hover:underline">Restock</button></td>
        </tr>
      `).join('');
    }}

    renderProducts(products);
  </script>
</body>
</html>"""

    return {
        "index.html": html_preview,
        "README.md": f"# {title}\n\nGenerated by BuildPilot AI.\n\n## Features\n- Live Product catalog with real-time search & category tabs\n- Slide-over Shopping Cart drawer with qty calculations\n- Integrated Admin Analytics Dashboard with revenue metrics & inventory table\n- Fully responsive layout"
    }

def get_portfolio_files(title: str = "Alex Morgan — Senior Full Stack Engineer") -> Dict[str, str]:
    """Generates complete source code files for a modern developer portfolio with contact form."""
    html_preview = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-950 text-slate-100 font-sans antialiased selection:bg-blue-600 selection:text-white">
  <!-- Navbar -->
  <nav class="border-b border-slate-800/80 sticky top-0 z-40 bg-slate-950/80 backdrop-blur-md">
    <div class="max-w-6xl mx-auto px-4 h-16 flex items-center justify-between">
      <div class="font-black text-lg text-blue-400 tracking-wider font-mono">&lt;AlexDev /&gt;</div>
      <div class="flex items-center gap-6 text-sm font-medium">
        <a href="#projects" class="text-slate-400 hover:text-white transition-colors">Projects</a>
        <a href="#skills" class="text-slate-400 hover:text-white transition-colors">Skills</a>
        <a href="#contact" class="bg-blue-600 hover:bg-blue-500 text-white px-4 py-2 rounded-xl transition-colors">Contact Me</a>
      </div>
    </div>
  </nav>

  <!-- Hero Section -->
  <header class="max-w-5xl mx-auto px-4 py-20 text-center space-y-6">
    <div class="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-blue-500/10 border border-blue-500/20 text-blue-400 text-xs font-semibold">
      <span class="w-2 h-2 rounded-full bg-emerald-400 animate-pulse"></span> Available for Architecture & Development Roles
    </div>
    <h1 class="text-4xl sm:text-6xl font-black tracking-tight leading-tight">
      Architecting Resilient Distributed Systems & <span class="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400">Autonomous AI Agents</span>.
    </h1>
    <p class="max-w-2xl mx-auto text-slate-400 text-base sm:text-lg">
      10+ years engineering cloud backends, microservices, and reactive web applications with TypeScript, Python, FastAPI, and MongoDB.
    </p>
  </header>

  <!-- Projects Section -->
  <section id="projects" class="max-w-6xl mx-auto px-4 py-12">
    <div class="flex items-center justify-between mb-8">
      <div>
        <h2 class="text-2xl font-bold text-white">Featured Engineering Projects</h2>
        <p class="text-xs text-slate-400">Filter by core architecture or technology domain</p>
      </div>
      <div class="flex gap-2">
        <button onclick="filterProjects('all')" class="px-3 py-1 text-xs rounded-lg bg-blue-600 text-white font-semibold">All</button>
        <button onclick="filterProjects('AI')" class="px-3 py-1 text-xs rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white">AI Agents</button>
        <button onclick="filterProjects('Backend')" class="px-3 py-1 text-xs rounded-lg bg-slate-900 border border-slate-800 text-slate-400 hover:text-white">Cloud Backend</button>
      </div>
    </div>

    <div id="projects-grid" class="grid grid-cols-1 md:grid-cols-2 gap-6"></div>
  </section>

  <!-- Interactive Contact Form Section -->
  <section id="contact" class="max-w-xl mx-auto px-4 py-16">
    <div class="bg-slate-900/80 border border-slate-800 p-6 sm:p-8 rounded-3xl shadow-xl space-y-4">
      <h3 class="text-xl font-bold text-white text-center">Get In Touch</h3>
      <p class="text-xs text-slate-400 text-center">Direct message channel to my inbox</p>

      <form onsubmit="handleContact(event)" class="space-y-4">
        <div>
          <label class="block text-xs font-medium text-slate-400">Your Name</label>
          <input type="text" id="contact-name" required placeholder="Sarah Connor" class="mt-1 w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-sm text-white focus:ring-2 focus:ring-blue-500">
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-400">Email Address</label>
          <input type="email" id="contact-email" required placeholder="sarah@example.com" class="mt-1 w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-sm text-white focus:ring-2 focus:ring-blue-500">
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-400">Project Overview</label>
          <textarea id="contact-msg" required rows="3" placeholder="Tell me about your project requirements..." class="mt-1 w-full bg-slate-950 border border-slate-800 rounded-xl p-2.5 text-sm text-white focus:ring-2 focus:ring-blue-500"></textarea>
        </div>
        <button type="submit" class="w-full bg-blue-600 hover:bg-blue-500 text-white font-bold py-2.5 rounded-xl shadow transition-colors">
          Send Message
        </button>
      </form>
    </div>
  </section>

  <script>
    const projects = [
      {{ id: 1, title: "Autonomous Multi-Agent Orchestrator", category: "AI", desc: "Coordinated LLM agent mesh featuring dynamic task dependency resolution and self-healing checkpoints.", tags: ["Python", "FastAPI", "Gemini", "Docker"] }},
      {{ id: 2, title: "High-Throughput Event Streaming Core", category: "Backend", desc: "Processes 50k events/sec with sub-millisecond p99 latency using async pipelines and MongoDB sharding.", tags: ["TypeScript", "MongoDB", "Redis", "Kafka"] }}
    ];

    function renderProjects(items) {{
      const grid = document.getElementById('projects-grid');
      grid.innerHTML = items.map(p => `
        <div class="bg-slate-900 border border-slate-800/80 rounded-2xl p-6 hover:border-slate-700 transition-all space-y-3">
          <div class="flex items-center justify-between">
            <span class="text-xs font-mono text-blue-400 font-semibold">${{p.category}}</span>
            <span class="text-xs text-slate-500"><i class="fa-solid fa-code-branch"></i> v1.4</span>
          </div>
          <h4 class="text-lg font-bold text-white">${{p.title}}</h4>
          <p class="text-xs text-slate-400 leading-relaxed">${{p.desc}}</p>
          <div class="flex flex-wrap gap-1.5 pt-2">
            ${{p.tags.map(t => `<span class="bg-slate-800 text-slate-300 text-[10px] px-2 py-0.5 rounded-md font-mono">${{t}}</span>`).join('')}}
          </div>
        </div>
      `).join('');
    }}

    function filterProjects(cat) {{
      const filtered = cat === 'all' ? projects : projects.filter(p => p.category === cat);
      renderProjects(filtered);
    }}

    function handleContact(e) {{
      e.preventDefault();
      const name = document.getElementById('contact-name').value;
      alert(`Thank you, ${{name}}! Your message has been recorded.`);
      e.target.reset();
    }}

    renderProjects(projects);
  </script>
</body>
</html>"""

    return {
        "index.html": html_preview,
        "README.md": f"# {title}\n\nGenerated by BuildPilot AI.\n\n## Features\n- High-performance dark aesthetic with Tailwind CSS\n- Project showcase with domain filtering\n- Form validation with interactive alerts"
    }

def get_task_manager_files(title: str = "PulseFlow Kanban & Task Manager") -> Dict[str, str]:
    """Generates complete source code files for a Kanban Board task management application."""
    html_preview = f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
</head>
<body class="bg-slate-100 text-slate-900 font-sans antialiased h-screen flex flex-col overflow-hidden">
  <!-- Top Navigation -->
  <header class="bg-white border-b border-slate-200 px-6 h-14 flex items-center justify-between shrink-0">
    <div class="flex items-center gap-3">
      <div class="w-8 h-8 rounded-lg bg-sky-600 flex items-center justify-center text-white font-bold text-sm">P</div>
      <span class="font-extrabold text-base tracking-tight">{title}</span>
    </div>
    <div class="flex items-center gap-3">
      <button onclick="openNewTaskModal()" class="bg-sky-600 hover:bg-sky-500 text-white font-semibold text-xs px-3.5 py-1.5 rounded-lg shadow-sm transition-colors flex items-center gap-1.5">
        <i class="fa-solid fa-plus"></i> New Task
      </button>
    </div>
  </header>

  <!-- Kanban Columns Area -->
  <main class="flex-1 p-6 overflow-x-auto flex gap-6 items-start">
    <!-- To Do -->
    <div class="w-80 bg-slate-200/70 rounded-2xl p-4 shrink-0 flex flex-col max-h-full">
      <div class="flex items-center justify-between mb-3">
        <span class="font-bold text-xs uppercase tracking-wider text-slate-600">To Do</span>
        <span id="count-todo" class="bg-slate-300 text-slate-700 text-xs font-bold px-2 py-0.5 rounded-full">0</span>
      </div>
      <div id="col-todo" class="space-y-3 overflow-y-auto flex-1"></div>
    </div>

    <!-- In Progress -->
    <div class="w-80 bg-slate-200/70 rounded-2xl p-4 shrink-0 flex flex-col max-h-full">
      <div class="flex items-center justify-between mb-3">
        <span class="font-bold text-xs uppercase tracking-wider text-sky-700">In Progress</span>
        <span id="count-in_progress" class="bg-sky-200 text-sky-800 text-xs font-bold px-2 py-0.5 rounded-full">0</span>
      </div>
      <div id="col-in_progress" class="space-y-3 overflow-y-auto flex-1"></div>
    </div>

    <!-- Completed -->
    <div class="w-80 bg-slate-200/70 rounded-2xl p-4 shrink-0 flex flex-col max-h-full">
      <div class="flex items-center justify-between mb-3">
        <span class="font-bold text-xs uppercase tracking-wider text-emerald-700">Completed</span>
        <span id="count-completed" class="bg-emerald-200 text-emerald-800 text-xs font-bold px-2 py-0.5 rounded-full">0</span>
      </div>
      <div id="col-completed" class="space-y-3 overflow-y-auto flex-1"></div>
    </div>
  </main>

  <!-- New Task Modal -->
  <div id="task-modal" class="fixed inset-0 z-50 hidden bg-black/50 backdrop-blur-xs flex items-center justify-center p-4">
    <div class="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl space-y-4">
      <div class="flex justify-between items-center border-b pb-3">
        <h3 class="font-bold text-base">Create New Task</h3>
        <button onclick="closeNewTaskModal()" class="text-slate-400 hover:text-slate-600"><i class="fa-solid fa-xmark"></i></button>
      </div>
      <form onsubmit="handleCreateTask(event)" class="space-y-3 text-sm">
        <div>
          <label class="block text-xs font-medium text-slate-700">Task Title</label>
          <input type="text" id="task-title" required placeholder="e.g., Integrate OAuth provider" class="mt-1 w-full border border-slate-300 rounded-lg p-2 text-sm focus:ring-2 focus:ring-sky-500">
        </div>
        <div>
          <label class="block text-xs font-medium text-slate-700">Priority</label>
          <select id="task-priority" class="mt-1 w-full border border-slate-300 rounded-lg p-2 text-sm focus:ring-2 focus:ring-sky-500">
            <option value="high">High Priority</option>
            <option value="medium" selected>Medium Priority</option>
            <option value="low">Low Priority</option>
          </select>
        </div>
        <button type="submit" class="w-full bg-sky-600 hover:bg-sky-500 text-white font-bold py-2.5 rounded-lg transition-colors">
          Add Task to Board
        </button>
      </form>
    </div>
  </div>

  <script>
    let tasks = [
      {{ id: 1, title: "Implement MongoDB connection pooling", status: "completed", priority: "high" }},
      {{ id: 2, title: "Build responsive Kanban drag preview", status: "in_progress", priority: "high" }},
      {{ id: 3, title: "Configure Docker compose multi-service stack", status: "todo", priority: "medium" }}
    ];

    function renderTasks() {{
      const cols = {{ todo: [], in_progress: [], completed: [] }};
      tasks.forEach(t => cols[t.status].push(t));

      ['todo', 'in_progress', 'completed'].forEach(col => {{
        document.getElementById(`count-${{col}}`).textContent = cols[col].length;
        const container = document.getElementById(`col-${{col}}`);
        container.innerHTML = cols[col].map(t => `
          <div class="bg-white p-3.5 rounded-xl border border-slate-200 shadow-sm space-y-2">
            <div class="flex items-center justify-between">
              <span class="text-[10px] font-bold px-2 py-0.5 rounded-full ${{
                t.priority === 'high' ? 'bg-red-100 text-red-700' :
                t.priority === 'medium' ? 'bg-amber-100 text-amber-700' : 'bg-slate-100 text-slate-600'
              }}">${{t.priority.toUpperCase()}}</span>
              <button onclick="deleteTask(${{t.id}})" class="text-slate-300 hover:text-red-500 text-xs"><i class="fa-solid fa-trash"></i></button>
            </div>
            <p class="font-medium text-xs text-slate-800 leading-snug">${{t.title}}</p>
            <div class="flex justify-between items-center pt-2 border-t border-slate-100 text-[11px]">
              <span class="text-slate-400">Move:</span>
              <div class="flex gap-1">
                ${{col !== 'todo' ? `<button onclick="moveTask(${{t.id}}, 'todo')" class="hover:text-sky-600 font-bold">To Do</button>` : ''}}
                ${{col !== 'in_progress' ? `<button onclick="moveTask(${{t.id}}, 'in_progress')" class="hover:text-sky-600 font-bold">Progress</button>` : ''}}
                ${{col !== 'completed' ? `<button onclick="moveTask(${{t.id}}, 'completed')" class="hover:text-emerald-600 font-bold">Done</button>` : ''}}
              </div>
            </div>
          </div>
        `).join('');
      }});
    }}

    function moveTask(id, newStatus) {{
      const task = tasks.find(t => t.id === id);
      if (task) {{ task.status = newStatus; renderTasks(); }}
    }}

    function deleteTask(id) {{
      tasks = tasks.filter(t => t.id !== id);
      renderTasks();
    }}

    function openNewTaskModal() {{ document.getElementById('task-modal').classList.remove('hidden'); }}
    function closeNewTaskModal() {{ document.getElementById('task-modal').classList.add('hidden'); }}

    function handleCreateTask(e) {{
      e.preventDefault();
      const title = document.getElementById('task-title').value;
      const priority = document.getElementById('task-priority').value;
      tasks.push({{ id: Date.now(), title, status: 'todo', priority }});
      closeNewTaskModal();
      document.getElementById('task-title').value = '';
      renderTasks();
    }}

    renderTasks();
  </script>
</body>
</html>"""

    return {
        "index.html": html_preview,
        "README.md": f"# {title}\n\nGenerated by BuildPilot AI.\n\n## Features\n- 3-column interactive Kanban workflow\n- Task movement, deletion, and priority badge styling\n- Dynamic task counter indicators"
    }

def get_project_files_by_archetype(archetype: str, title: str) -> Dict[str, str]:
    if archetype == "hotel_booking":
        return get_hotel_booking_files(title)
    elif archetype == "ecommerce":
        return get_ecommerce_files(title)
    elif archetype == "portfolio":
        return get_portfolio_files(title)
    else:
        return get_task_manager_files(title)
