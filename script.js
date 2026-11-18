const toggle = document.querySelector('.menu-toggle');
const nav = document.querySelector('.main-nav');

// API base URL - change this to your server URL
const API_URL = '/api';

toggle?.addEventListener('click', () => {
  const open = nav.classList.toggle('open');
  toggle.setAttribute('aria-expanded', String(open));
  toggle.setAttribute('aria-label', open ? 'Close navigation' : 'Open navigation');
});

document.querySelectorAll('.main-nav a').forEach((link) => {
  link.addEventListener('click', () => {
    nav.classList.remove('open');
    toggle?.setAttribute('aria-expanded', 'false');
  });
});

// ==================== API FUNCTIONS ====================

/**
 * Submit contact form
 */
async function submitContact(formData) {
  try {
    const response = await fetch(`${API_URL}/contact/submit`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Failed to submit contact form');
    }
    
    return data;
  } catch (error) {
    console.error('Contact form error:', error);
    throw new Error(error.name === 'TypeError'
      ? 'Cannot connect to the backend. Start the API with "python app.py" and try again.'
      : error.message);
  }
}

/**
 * Submit demo/quote request
 */
async function submitDemoRequest(formData) {
  try {
    const response = await fetch(`${API_URL}/demo/request`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(formData),
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Failed to submit demo request');
    }
    
    return data;
  } catch (error) {
    console.error('Demo request error:', error);
    throw error;
  }
}

/**
 * User registration
 */
async function registerUser(email, username, password, fullName) {
  try {
    const response = await fetch(`${API_URL}/auth/register`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        username,
        password,
        full_name: fullName,
      }),
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Registration failed');
    }
    
    return data;
  } catch (error) {
    console.error('Registration error:', error);
    throw error;
  }
}

/**
 * User login
 */
async function loginUser(email, password) {
  try {
    const response = await fetch(`${API_URL}/auth/login`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        email,
        password,
      }),
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Login failed');
    }
    
    return data;
  } catch (error) {
    console.error('Login error:', error);
    throw error;
  }
}

/**
 * Get all products
 */
async function getProducts(category = null) {
  try {
    let url = `${API_URL}/products`;
    if (category) {
      url += `?category=${category}`;
    }
    
    const response = await fetch(url);
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Failed to fetch products');
    }
    
    return data;
  } catch (error) {
    console.error('Products fetch error:', error);
    throw error;
  }
}

/**
 * Get single product
 */
async function getProduct(productId) {
  try {
    const response = await fetch(`${API_URL}/products/${productId}`);
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Product not found');
    }
    
    return data;
  } catch (error) {
    console.error('Product fetch error:', error);
    throw error;
  }
}

/**
 * Create an order
 */
async function createOrder(customerName, customerEmail, productId, options = {}) {
  try {
    const response = await fetch(`${API_URL}/orders`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        customer_name: customerName,
        customer_email: customerEmail,
        product_id: productId,
        customer_phone: options.customerPhone || '',
        description: options.description || '',
      }),
    });
    
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Failed to create order');
    }
    
    return data;
  } catch (error) {
    console.error('Order creation error:', error);
    throw error;
  }
}

/**
 * Get order status
 */
async function getOrder(orderId) {
  try {
    const response = await fetch(`${API_URL}/orders/${orderId}`);
    const data = await response.json();
    
    if (!response.ok) {
      throw new Error(data.error || 'Order not found');
    }
    
    return data;
  } catch (error) {
    console.error('Order fetch error:', error);
    throw error;
  }
}

/**
 * Check API health
 */
async function checkHealth() {
  try {
    const response = await fetch(`${API_URL}/health`);
    const data = await response.json();
    return data.status === 'healthy';
  } catch (error) {
    console.error('Health check failed:', error);
    return false;
  }
}

async function getProject(slug) {
  const response = await fetch(`${API_URL}/projects/${slug}`);
  const data = await response.json();
  if (!response.ok) throw new Error(data.error || 'Project not found');
  return data;
}

function focusContact(subject = '') {
  const form = document.querySelector('#contact-form');
  if (form) {
    form.elements.subject.value = subject;
    document.querySelector('#contact')?.scrollIntoView({ behavior: 'smooth' });
    form.elements.name.focus({ preventScroll: true });
  }
}

document.addEventListener('DOMContentLoaded', () => {
  document.querySelectorAll('.js-contact-button').forEach((button) => {
    button.addEventListener('click', () => focusContact());
  });

  document.querySelectorAll('.js-demo-button').forEach((button) => {
    button.addEventListener('click', () => focusContact('Request a free demo'));
  });

  document.querySelectorAll('.js-project-button').forEach((button) => {
    button.addEventListener('click', async () => {
      button.disabled = true;
      try {
        const project = await getProject(button.dataset.project);
        focusContact(`Project enquiry: ${project.name}`);
      } catch (error) {
        console.error('Project fetch error:', error);
        focusContact();
      } finally {
        button.disabled = false;
      }
    });
  });

  document.querySelector('#contact-form')?.addEventListener('submit', async (event) => {
    event.preventDefault();
    const form = event.currentTarget;
    const status = form.querySelector('.form-status');
    const submitButton = form.querySelector('button[type="submit"]');
    submitButton.disabled = true;
    status.textContent = 'Sending...';
    try {
      await submitContact(Object.fromEntries(new FormData(form)));
      form.reset();
      status.textContent = 'Thanks. We received your message and will be in touch.';
    } catch (error) {
      status.textContent = error.message;
    } finally {
      submitButton.disabled = false;
    }
  });
});
