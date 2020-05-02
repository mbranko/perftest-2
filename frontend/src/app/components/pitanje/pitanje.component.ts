import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { TestService } from '../../services/test.service';
import { Pitanje } from '../../models';
import { FormBuilder, FormGroup, Validators } from '@angular/forms';
import { MatSnackBar } from '@angular/material/snack-bar';
import { stringify } from 'querystring';

@Component({
  selector: 'app-pitanje',
  templateUrl: './pitanje.component.html',
  styleUrls: ['./pitanje.component.scss']
})
export class PitanjeComponent implements OnInit {

  redniBroj: number;
  pitanje: Pitanje;
  formGroup: FormGroup;

  constructor(
      private fb: FormBuilder,
      private activatedRoute: ActivatedRoute,
      private router: Router,
      private snackBar: MatSnackBar,
      private testService: TestService
  ) {}

  ngOnInit(): void {
    this.activatedRoute.params.subscribe(params => {
      this.redniBroj = +params.rbr;
      this.pitanje = this.testService.test.pitanje_set[this.redniBroj - 1];
    });
    this.formGroup = this.fb.group({
      odgovor: ['', Validators.required]});
  }

  prethodno(): void {
    if (this.formGroup.valid) {
      this.posaljiOdgovor(['/pitanje', this.redniBroj - 1]);
    } else {
      const snackBarRef = this.snackBar.open('Odgovor nije popunjen!', 'OK');
    }
  }

  sledece(): void {
    if (this.formGroup.valid) {
      this.posaljiOdgovor(['/pitanje', this.redniBroj + 1]);
    } else {
      const snackBarRef = this.snackBar.open('Odgovor nije popunjen!', 'OK');
    }
  }

  zavrsi(): void {
    if (this.formGroup.valid) {
      this.posaljiOdgovor(['/finish']);
    } else {
      const snackBarRef = this.snackBar.open('Odgovor nije popunjen!', 'OK');
    }
  }

  posaljiOdgovor(narednaRuta: any[]): void {
      const testUcenika = JSON.parse(sessionStorage.getItem('testUcenika'));
      const odgovor = this.formGroup.get('odgovor').value;
      this.formGroup.reset();
      this.testService.posaljiOdgovor(testUcenika, this.pitanje.id, odgovor).subscribe(data => {
        this.router.navigate(narednaRuta);
      }, error => {
        const snackBarRef = this.snackBar.open(`Greška ${error.status}!`, 'OK');
        console.log(error);
      });
  }

  nextButtonLabel(): string {
    return (this.redniBroj === 20) ? 'Završi test' : 'Sledeće pitanje';
  }
}
