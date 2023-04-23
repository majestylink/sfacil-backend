import { Component, OnInit } from '@angular/core';
import { CustomerService } from '../customer.service';
import { ApiResponse, Customer } from '../myModels';
import { Subscription } from 'rxjs';

@Component({
  selector: 'app-customer',
  templateUrl: './customer.component.html',
  styleUrls: ['./customer.component.css']
})
export class CustomerComponent implements OnInit {
  customers: Customer[] = [];
  subscription: Subscription | undefined;

  constructor(private customerService: CustomerService) { }

  ngOnInit(): void {
    this.customerService.getCustomers().subscribe({
      next: (data: ApiResponse<Customer[]>) => {
        this.customers = data.data;
        console.log(this.customers);
        
      },
      error: (error: any) => {
        console.error('Error fetching customers', error);
      },
      complete: () => {
        console.log('Finished fetching customers');
      }
    });
  }

  ngOnDestroy(): void {
    if (this.subscription) {
      this.subscription.unsubscribe();
    }
  }
}
