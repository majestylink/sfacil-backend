import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { PurchasesService } from '../purchases.service';
import { Purchase } from '../myModels';
import { NgbModal, NgbModalRef } from '@ng-bootstrap/ng-bootstrap';


@Component({
  selector: 'app-purchases',
  templateUrl: './purchases.component.html',
  styleUrls: ['./purchases.component.css']
})
export class PurchasesComponent implements OnInit {
  modalRef: NgbModalRef | undefined;
  

  customerId: number;
  customerName: string = '';
  purchases: Purchase[] = [];
  orderedProducts:any = []

  constructor(private route: ActivatedRoute, private purchaseService: PurchasesService, private modalService: NgbModal) {
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

  openModal(content: any) {
    this.modalRef = this.modalService.open(content);
  }

}
