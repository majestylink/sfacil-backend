export interface Customer {
    id: string;
    first_name: string;
    last_name: string;
    other_name: string;
    image: string;
    address: string;
    phone: string;
    email: string;
    created_at: string;
    updated_at: string;
  }

export interface ApiResponse<T> {
    results: any;
    status: boolean;
    message: string;
    data: T;
  }

export  interface Purchase {
    customer: string;
    fulfilled: boolean;
    cost: number | null;
    created_at: string;
    ordered_products: {
      mattresses: {
        id: number;
        product: {
          id: number;
          product_category: {
            id: number;
            name: string;
          };
          product_id: string;
          inches: string;
          dimensions: string;
          price: string;
        };
        quantity: number;
      }[];
    }[];
  }