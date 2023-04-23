import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { ApiResponse, Customer } from './myModels';

@Injectable({
  providedIn: 'root'
})
export class CustomerService {

  private baseUrl = 'http://localhost:8000/api/';

  constructor(private http: HttpClient) { }

  getCustomers(): Observable<ApiResponse<Customer[]>> {
    const url = this.baseUrl + 'customers/';
    return this.http.get<ApiResponse<Customer[]>>(url);
  }
}