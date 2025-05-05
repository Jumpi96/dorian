import React, { useState, useEffect } from 'react';
import { wardrobeService } from '../services/wardrobeService';

const WardrobePage = () => {
    const [items, setItems] = useState([]);
    const [newItem, setNewItem] = useState('');
    const [error, setError] = useState(null);
    const [loading, setLoading] = useState(false);

    useEffect(() => {
        fetchItems();
    }, []);

    const fetchItems = async () => {
        try {
            setLoading(true);
            const data = await wardrobeService.getItems();
            setItems(data.items);
            setError(null);
        } catch (err) {
            setError('Failed to load wardrobe items');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        if (!newItem.trim()) return;

        try {
            setLoading(true);
            await wardrobeService.addItem(newItem.trim());
            setNewItem('');
            await fetchItems(); // Refresh the list
            setError(null);
        } catch (err) {
            setError('Failed to add item');
            console.error(err);
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="max-w-2xl mx-auto p-4">
            <h1 className="text-2xl font-bold mb-4">My Wardrobe</h1>
            
            {/* Add Item Form */}
            <form onSubmit={handleSubmit} className="mb-6">
                <div className="flex gap-2">
                    <input
                        type="text"
                        value={newItem}
                        onChange={(e) => setNewItem(e.target.value)}
                        placeholder="Add a new item (e.g., blue jeans)"
                        className="flex-1 p-2 border rounded"
                        disabled={loading}
                    />
                    <button
                        type="submit"
                        className="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 disabled:bg-blue-300"
                        disabled={loading || !newItem.trim()}
                    >
                        Add
                    </button>
                </div>
            </form>

            {/* Error Message */}
            {error && (
                <div className="bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded mb-4">
                    {error}
                </div>
            )}

            {/* Loading State */}
            {loading && (
                <div className="text-center py-4">
                    Loading...
                </div>
            )}

            {/* Items List */}
            <div className="space-y-2">
                {items.map((item) => (
                    <div
                        key={item.itemId}
                        className="p-3 bg-white border rounded shadow-sm"
                    >
                        {item.description}
                    </div>
                ))}
            </div>

            {/* Empty State */}
            {!loading && items.length === 0 && (
                <div className="text-center text-gray-500 py-4">
                    Your wardrobe is empty. Add some items to get started!
                </div>
            )}
        </div>
    );
};

export default WardrobePage; 