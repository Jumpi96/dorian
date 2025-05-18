export type InteractionType = 'outfit_recommendation' | 'purchase_recommendation' | 'trip';

export interface BaseInteraction {
  createdAt: string;
  interactionId: string;
  type: InteractionType;
  userId: string;
}

export interface OutfitRecommendation extends BaseInteraction {
  type: 'outfit_recommendation';
  situation: string;
  recommendation: {
    top: string;
    bottom: string;
    outerwear: string;
    shoes: string;
  };
  tripId?: string;
}

export interface PurchaseRecommendation extends BaseInteraction {
  type: 'purchase_recommendation';
  situation: string;
  recommendation: {
    item: string;
    explanation: string;
  };
}

export interface TripRecommendation extends BaseInteraction {
  type: 'trip';
  description: string;
  recommendation: {
    packingList: {
      tops: string[];
      bottoms: string[];
      outerwear: string[];
      shoes: string[];
      accessories: string[];
    };
  };
}

export type Interaction = OutfitRecommendation | PurchaseRecommendation | TripRecommendation; 