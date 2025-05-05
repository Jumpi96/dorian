const API_BASE_URL = 'http://localhost:3001';

export const wardrobeService = {
    async getItems() {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/wardrobe`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });
        
        if (!response.ok) {
            throw new Error('Failed to fetch wardrobe items');
        }
        
        return response.json();
    },
    
    async addItem(description) {
        const token = localStorage.getItem('token');
        const response = await fetch(`${API_BASE_URL}/wardrobe/add`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ description })
        });
        
        if (!response.ok) {
            throw new Error('Failed to add wardrobe item');
        }
        
        return response.json();
    }
}; 