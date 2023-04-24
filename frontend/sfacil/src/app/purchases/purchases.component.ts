import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { PurchasesService } from '../purchases.service';
import { Purchase } from '../myModels';


@Component({
  selector: 'app-purchases',
  templateUrl: './purchases.component.html',
  styleUrls: ['./purchases.component.css']
})
export class PurchasesComponent implements OnInit {
  

  customerId: number;
  customerName: string = '';
  purchases: Purchase[] = [];
  orderedProducts:any = []

  constructor(private route: ActivatedRoute, private purchaseService: PurchasesService) {
    this.customerId = 0;
  }

  ngOnInit(): void {
    this.customerId = this.route.snapshot.params['customerId'];
    this.purchaseService.getCustomerPurchases(this.customerId).subscribe((purchases: any) => {
      this.purchases = purchases["data"];
      this.customerName = purchases["data"][0]['customer'];
      console.log(this.purchases);
      
    });
  }

}
