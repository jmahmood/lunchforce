webpackJsonp(["main"],{

/***/ "../../../../../src/$$_gendir lazy recursive":
/***/ (function(module, exports) {

function webpackEmptyAsyncContext(req) {
	// Here Promise.resolve().then() is used instead of new Promise() to prevent
	// uncatched exception popping up in devtools
	return Promise.resolve().then(function() {
		throw new Error("Cannot find module '" + req + "'.");
	});
}
webpackEmptyAsyncContext.keys = function() { return []; };
webpackEmptyAsyncContext.resolve = webpackEmptyAsyncContext;
module.exports = webpackEmptyAsyncContext;
webpackEmptyAsyncContext.id = "../../../../../src/$$_gendir lazy recursive";

/***/ }),

/***/ "../../../../../src/app/app.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ".ng-valid[required], .ng-valid.required  {\n  border-left: 5px solid #42A948; /* green */\n}\n\n.ng-invalid:not(form)  {\n  border-left: 5px solid #a94442; /* red */\n}\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/app.component.html":
/***/ (function(module, exports) {

module.exports = "  <nav class=\"navbar navbar-default\">\n    <app-nav></app-nav>\n  </nav>\n  <div class=\"container\" [ngSwitch]=\"navService.state\">\n    <div *ngSwitchCase=\"'waiting'\">\n      <img alt=\"LunchForce\" src=\"assets/index.coin-flowing-loader.svg\">\n      Waiting..\n    </div>\n\n    <div *ngSwitchCase=\"'loadmyevents'\">\n        <img alt=\"LunchForce\" src=\"assets/index.money-coin-palette-color-preloader.svg\">\n      loading your upcoming lunch data...\n    </div>\n\n    <div *ngSwitchCase=\"'enrollment'\">\n      <app-enrollment [foodOptions]=\"foodOptions\" [locationOptions]=\"locationOptions\"></app-enrollment>\n    </div>\n\n    <div *ngSwitchCase=\"'login'\">\n      <app-login (loginEvent)=\"onLogin($event)\"></app-login>\n    </div>\n\n    <div *ngSwitchCase=\"'search'\" class=\"search\">\n      <app-search [foodOptions]=\"foodOptions\" [locationOptions]=\"locationOptions\"></app-search>\n\n    </div>\n\n    <div *ngSwitchCase=\"'introduction'\">\n      <app-introduction></app-introduction>\n    </div>\n\n    <div *ngSwitchCase=\"'introductionsuccess'\">\n      <app-invitation-success></app-invitation-success>\n    </div>\n\n    <div *ngSwitchCase=\"'profile'\">\n      <app-my-profile [foodOptions]=\"foodOptions\" [locationOptions]=\"locationOptions\"></app-my-profile>\n    </div>\n\n    <div *ngSwitchCase=\"'myevents'\">\n      <app-my-events></app-my-events>\n    </div>\n\n    <div *ngSwitchCase=\"'availability'\">\n          <app-availability></app-availability>\n    </div>\n\n    <div *ngSwitchCase=\"'publicevents'\">\n      <div class=\"alert alert-error\" role=\"alert\" [hidden]=\"!joinedAppointment\">\n        <span class=\"glyphicon glyphicon-exclamation-sign\" aria-hidden=\"true\"></span>\n        <span class=\"sr-only\">Successfully joined:</span>\n        You successfully joined the event (xxx)\n      </div>\n      <app-appointment-item [appointments]=\"appointmentService.everyoneAppointments.appointments\" [allowJoiningEvent]=true (joinEvent)=\"onAppointmentJoined($event)\">\n        There are no public events currently available.\n      </app-appointment-item>\n    </div>\n\n    <div *ngSwitchCase=\"'invitedto'\">\n      <div class=\"alert alert-error\" role=\"alert\" [hidden]=\"!joinedAppointment\">\n        <span class=\"glyphicon glyphicon-exclamation-sign\" aria-hidden=\"true\"></span>\n        <span class=\"sr-only\">Successfully joined:</span>\n        You successfully joined the event (xxx)\n      </div>\n      <app-appointment-item [appointments]=\"appointmentService.myInvitations.appointments\" [allowJoiningEvent]=true (joinEvent)=\"onAppointmentJoined($event)\">\n        There are no invitations outstanding for you.\n      </app-appointment-item>\n    </div>\n\n    <ng-template #errorModal>\n      <div class=\"modal-header\">\n        <h4 class=\"modal-title pull-left\">Modal</h4>\n        <button type=\"button\" class=\"close pull-right\" aria-label=\"Close\" (click)=\"modalRef.hide()\">\n          <span aria-hidden=\"true\">&times;</span>\n        </button>\n      </div>\n      <div class=\"modal-body\">\n        {{errormodal_message}}\n      </div>\n    </ng-template>\n\n</div>\n"

/***/ }),

/***/ "../../../../../src/app/app.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1_ngx_bootstrap__ = __webpack_require__("../../../../ngx-bootstrap/index.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__appointment_service__ = __webpack_require__("../../../../../src/app/appointment.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__auth_service__ = __webpack_require__("../../../../../src/app/auth.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__init_service__ = __webpack_require__("../../../../../src/app/init.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5__nav_service__ = __webpack_require__("../../../../../src/app/nav.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6_ngx_cookie_service__ = __webpack_require__("../../../../ngx-cookie-service/index.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};







let AppComponent = class AppComponent {
    constructor(modalService, authService, appointmentService, initService, navService, cookieService) {
        this.modalService = modalService;
        this.authService = authService;
        this.appointmentService = appointmentService;
        this.initService = initService;
        this.navService = navService;
        this.cookieService = cookieService;
        this.joinedAppointment = false;
    }
    openModal(template) {
        this.modalRef = this.modalService.show(template);
    }
    appointments() {
        if (this.navService.is('myevents')) {
            return this.appointmentService.myAppointments.appointments;
        }
        if (this.navService.is('publicevents')) {
            return this.appointmentService.everyoneAppointments.appointments;
        }
        if (this.navService.is('search') && this.appointmentService.searchResults) {
            return this.appointmentService.searchResults.youonly.concat(this.appointmentService.searchResults.everyone);
        }
    }
    onAppointmentJoined() {
        this.navService.myevents();
        this.joinedAppointment = true;
        setTimeout(() => { this.joinedAppointment = false; }, 1000);
    }
    onLogin(data) {
        console.log(data);
        this.authService.send_login(data).then(() => {
            console.log('Emitting event');
            this.onLoginTokenSet();
        });
    }
    ;
    onLoginTokenSet() {
        console.log('Event caught.');
        this.postLoginSetup().then(() => {
            this.navService.myevents();
            this.cookieService.set('login_token', this.authService.token);
        }).catch((err) => {
            this.navService.login();
            if (err.status === 0) {
                this.authService.login.error_messages = ['Could not connect to server'];
            }
            console.log(err);
        });
    }
    postLoginSetup() {
        this.navService.loadmyevents();
        const p1 = this.appointmentService.my(this.authService.token);
        const p2 = this.appointmentService.everyone(this.authService.token);
        const p3 = this.appointmentService.available(this.authService.token);
        const p4 = this.authService.my_profile();
        const p5 = this.appointmentService.invitations(this.authService.token);
        return Promise.all([p1, p2, p3, p4, p5]);
    }
    ngOnInit() {
        this.authService.clear();
        this.navService.login();
        this.foodOptions = [];
        this.initService.food_options().then(res => {
            this.foodOptions = res.food_options;
            console.log(this.foodOptions);
            return res;
        }).catch(err => {
            console.log('could not load food options');
            console.log(err);
        });
        this.locationOptions = [];
        this.initService.locations().then(res => {
            this.locationOptions = res.locations;
            console.log(this.locationOptions);
            return res;
        }).catch(err => {
            console.log('could not load food options');
            console.log(err);
        });
        if (this.authService.check_cookies(this.cookieService)) {
            console.log('We have a cookie set with the token information.');
            this.onLoginTokenSet();
        }
    }
};
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_13" /* ViewChild */])('errorModal'),
    __metadata("design:type", typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_0__angular_core__["_9" /* TemplateRef */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_0__angular_core__["_9" /* TemplateRef */]) === "function" && _a || Object)
], AppComponent.prototype, "errorModal", void 0);
AppComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
        selector: 'app-root',
        template: __webpack_require__("../../../../../src/app/app.component.html"),
        styles: [__webpack_require__("../../../../../src/app/app.component.css")],
        providers: [__WEBPACK_IMPORTED_MODULE_2__appointment_service__["a" /* AppointmentService */], __WEBPACK_IMPORTED_MODULE_3__auth_service__["a" /* AuthService */], __WEBPACK_IMPORTED_MODULE_4__init_service__["a" /* InitService */], __WEBPACK_IMPORTED_MODULE_5__nav_service__["a" /* NavService */]]
    }),
    __metadata("design:paramtypes", [typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_1_ngx_bootstrap__["a" /* BsModalService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1_ngx_bootstrap__["a" /* BsModalService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_3__auth_service__["a" /* AuthService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__auth_service__["a" /* AuthService */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_2__appointment_service__["a" /* AppointmentService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__appointment_service__["a" /* AppointmentService */]) === "function" && _d || Object, typeof (_e = typeof __WEBPACK_IMPORTED_MODULE_4__init_service__["a" /* InitService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4__init_service__["a" /* InitService */]) === "function" && _e || Object, typeof (_f = typeof __WEBPACK_IMPORTED_MODULE_5__nav_service__["a" /* NavService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_5__nav_service__["a" /* NavService */]) === "function" && _f || Object, typeof (_g = typeof __WEBPACK_IMPORTED_MODULE_6_ngx_cookie_service__["a" /* CookieService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_6_ngx_cookie_service__["a" /* CookieService */]) === "function" && _g || Object])
], AppComponent);

var _a, _b, _c, _d, _e, _f, _g;
//# sourceMappingURL=app.component.js.map

/***/ }),

/***/ "../../../../../src/app/app.module.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppModule; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser__ = __webpack_require__("../../../platform-browser/@angular/platform-browser.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__app_component__ = __webpack_require__("../../../../../src/app/app.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__angular_forms__ = __webpack_require__("../../../forms/@angular/forms.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__angular_common_http__ = __webpack_require__("../../../common/@angular/common/http.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_5_ngx_bootstrap__ = __webpack_require__("../../../../ngx-bootstrap/index.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_6__salesforce_only_directive__ = __webpack_require__("../../../../../src/app/salesforce-only.directive.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_7__appointment_item_appointment_item_component__ = __webpack_require__("../../../../../src/app/appointment-item/appointment-item.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_8__availability_availability_component__ = __webpack_require__("../../../../../src/app/availability/availability.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_9__my_profile_my_profile_component__ = __webpack_require__("../../../../../src/app/my-profile/my-profile.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_10__introduction_introduction_component__ = __webpack_require__("../../../../../src/app/introduction/introduction.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_11__invitation_success_invitation_success_component__ = __webpack_require__("../../../../../src/app/invitation-success/invitation-success.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_12__enrollment_enrollment_component__ = __webpack_require__("../../../../../src/app/enrollment/enrollment.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_13__my_events_my_events_component__ = __webpack_require__("../../../../../src/app/my-events/my-events.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_14__search_search_component__ = __webpack_require__("../../../../../src/app/search/search.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_15__nav_nav_component__ = __webpack_require__("../../../../../src/app/nav/nav.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_16__login_login_component__ = __webpack_require__("../../../../../src/app/login/login.component.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_17_ngx_cookie_service__ = __webpack_require__("../../../../ngx-cookie-service/index.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};


















let AppModule = class AppModule {
};
AppModule = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_1__angular_core__["L" /* NgModule */])({
        declarations: [
            __WEBPACK_IMPORTED_MODULE_2__app_component__["a" /* AppComponent */],
            __WEBPACK_IMPORTED_MODULE_6__salesforce_only_directive__["a" /* SalesforceOnlyDirective */],
            __WEBPACK_IMPORTED_MODULE_7__appointment_item_appointment_item_component__["a" /* AppointmentItemComponent */],
            __WEBPACK_IMPORTED_MODULE_8__availability_availability_component__["a" /* AvailabilityComponent */],
            __WEBPACK_IMPORTED_MODULE_9__my_profile_my_profile_component__["a" /* MyProfileComponent */],
            __WEBPACK_IMPORTED_MODULE_10__introduction_introduction_component__["a" /* IntroductionComponent */],
            __WEBPACK_IMPORTED_MODULE_11__invitation_success_invitation_success_component__["a" /* InvitationSuccessComponent */],
            __WEBPACK_IMPORTED_MODULE_12__enrollment_enrollment_component__["a" /* EnrollmentComponent */],
            __WEBPACK_IMPORTED_MODULE_13__my_events_my_events_component__["a" /* MyEventsComponent */],
            __WEBPACK_IMPORTED_MODULE_14__search_search_component__["a" /* SearchComponent */],
            __WEBPACK_IMPORTED_MODULE_15__nav_nav_component__["a" /* NavComponent */],
            __WEBPACK_IMPORTED_MODULE_16__login_login_component__["a" /* LoginComponent */],
        ],
        imports: [
            __WEBPACK_IMPORTED_MODULE_0__angular_platform_browser__["a" /* BrowserModule */],
            __WEBPACK_IMPORTED_MODULE_3__angular_forms__["a" /* FormsModule */],
            __WEBPACK_IMPORTED_MODULE_4__angular_common_http__["b" /* HttpClientModule */],
            __WEBPACK_IMPORTED_MODULE_5_ngx_bootstrap__["b" /* ModalModule */].forRoot(),
        ],
        providers: [__WEBPACK_IMPORTED_MODULE_17_ngx_cookie_service__["a" /* CookieService */]],
        bootstrap: [__WEBPACK_IMPORTED_MODULE_2__app_component__["a" /* AppComponent */]]
    })
], AppModule);

//# sourceMappingURL=app.module.js.map

/***/ }),

/***/ "../../../../../src/app/appointment-item/appointment-item.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/appointment-item/appointment-item.component.html":
/***/ (function(module, exports) {

module.exports = "<table class=\"table\" *ngIf=\"appointments && appointments.length > 0; else noResultsFound\">\n<tr>\n  <th>Name</th>\n  <th>Date</th>\n  <th>Location</th>\n  <th>People Attending</th>\n  <th *ngIf=\"allowJoiningEvent\">Status</th>\n</tr>\n<tr *ngFor=\"let app of appointments; let i=index\" [ngClass]=\"{'highlight': app.highlight}\">\n  <td>{{app.title}}</td>\n  <td>{{app.date | date:'yyyy-MM-dd'}}</td>\n  <td>{{app.location}}</td>\n  <td>\n    <div *ngIf=\"app.people.length > 0\">\n      <ul class=\"list-group\"><li class=\"list-group-item\" *ngFor=\"let peep of app.people\" (click)=\"lg(peep[0]);\">{{peep[1]}}</li></ul>\n    </div>\n  </td>\n  <td *ngIf=\"allowJoiningEvent\">\n      <button class=\"btn btn-info\" (click)=\"joinAppointment(app.id)\" *ngIf=\"app.space_available > 0; else NoSpaceAvailable\">Join</button>\n      <ng-template #NoSpaceAvailable>Event Full</ng-template>\n  </td>\n</tr>\n</table>\n<ng-template #noResultsFound>\n  <ng-content></ng-content>\n</ng-template>\n"

/***/ }),

/***/ "../../../../../src/app/appointment-item/appointment-item.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppointmentItemComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__appointment_service__ = __webpack_require__("../../../../../src/app/appointment.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__auth_service__ = __webpack_require__("../../../../../src/app/auth.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



let AppointmentItemComponent = class AppointmentItemComponent {
    constructor(appointmentService, authService) {
        this.appointmentService = appointmentService;
        this.authService = authService;
        this.allowJoiningEvent = false;
        this.joinEvent = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["w" /* EventEmitter */]();
    }
    joinAppointment(appointment_id) {
        this.appointmentService.attend(this.authService.token, appointment_id).then(() => {
            return this.appointmentService.my(this.authService.token); // My appointments are refreshed.
        }).then((res) => {
            /*  This stuff only affects this particular component. */
            for (const appointment of res.appointments) {
                if (appointment.id === appointment_id) {
                    appointment.highlight = true;
                }
            }
            this.joinEvent.emit(true);
        }).catch((err) => {
            console.log('Unhandled exception!');
            console.log(err);
        });
    }
    ngOnInit() { }
    lg(string) {
        console.log(string);
    }
};
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["E" /* Input */])(),
    __metadata("design:type", Array)
], AppointmentItemComponent.prototype, "appointments", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["E" /* Input */])(),
    __metadata("design:type", Object)
], AppointmentItemComponent.prototype, "allowJoiningEvent", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["R" /* Output */])(),
    __metadata("design:type", Object)
], AppointmentItemComponent.prototype, "joinEvent", void 0);
AppointmentItemComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
        selector: 'app-appointment-item',
        template: __webpack_require__("../../../../../src/app/appointment-item/appointment-item.component.html"),
        styles: [__webpack_require__("../../../../../src/app/appointment-item/appointment-item.component.css")],
        providers: []
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__appointment_service__["a" /* AppointmentService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__appointment_service__["a" /* AppointmentService */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_2__auth_service__["a" /* AuthService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__auth_service__["a" /* AuthService */]) === "function" && _b || Object])
], AppointmentItemComponent);

var _a, _b;
//# sourceMappingURL=appointment-item.component.js.map

/***/ }),

/***/ "../../../../../src/app/appointment.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AppointmentService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_common_http__ = __webpack_require__("../../../common/@angular/common/http.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_q__ = __webpack_require__("../../../../q/q.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_q___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_q__);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



// http://localhost:8000/api/my-appointments/
const SEARCH_URL = 'http://localhost:8000/api/search/';
const ATTEND_EVENT_URL = 'http://localhost:8000/api/attend/';
const MY_EVENTS_URL = 'http://localhost:8000/api/my-appointments/';
const PUBLIC_EVENTS_URL = 'http://localhost:8000/api/public-appointments/';
const INVITATEDTO_URL = 'http://localhost:8000/api/invitedto-appointments/';
const MY_AVAILABILITY_URL = 'http://localhost:8000/api/my-availability/';
const UPDATE_AVAILABILITY_URL = 'http://localhost:8000/api/update-availability/';
let AppointmentService = class AppointmentService {
    constructor(http) {
        this.http = http;
        // Accessing appointments happens from here.
        this.searchResults = null;
    }
    clear() {
        this.searchResults = null;
        this.myAppointments = null;
        this.myAvailability = null;
        this.everyoneAppointments = null;
    }
    set_availability_dates() {
        for (const avail of this.myAvailability.availability) {
            avail.date = new Date(avail.date_str);
        }
    }
    send_availability(auth_token, month, availableOn) {
        const token_header = new __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["c" /* HttpHeaders */]().set('Authorization', 'Token ' + auth_token);
        return this.http.post(UPDATE_AVAILABILITY_URL, { month: month, date: availableOn }, { 'headers': token_header }).toPromise().then((res) => {
            if (!res.success) {
                return Object(__WEBPACK_IMPORTED_MODULE_2_q__["reject"])(res.message);
            }
            console.log(res);
            this.myAvailability = { success: res.success, availability: res.availability, message: res.message };
            this.set_availability_dates();
            return res;
        });
    }
    available(auth_token) {
        const token_header = new __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["c" /* HttpHeaders */]().set('Authorization', 'Token ' + auth_token);
        return this.http.get(MY_AVAILABILITY_URL, { 'headers': token_header }).toPromise().then((res) => {
            this.myAvailability = res;
            this.set_availability_dates();
            console.log('my current availability');
            console.log(this.myAvailability);
            return res;
        });
    }
    search(auth_token, searchForm) {
        const token_header = new __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["c" /* HttpHeaders */]().set('Authorization', 'Token ' + auth_token);
        return this.http.post(SEARCH_URL, searchForm.value, { headers: token_header }).toPromise().then((res) => {
            console.log('Search results');
            console.log(res);
            if (!res.success) {
                return Object(__WEBPACK_IMPORTED_MODULE_2_q__["reject"])(res.message);
            }
            this.searchResults = res;
            console.log('search results');
            console.log(res);
            return res;
        });
    }
    attend(auth_token, appointment_id) {
        const token_header = new __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["c" /* HttpHeaders */]().set('Authorization', 'Token ' + auth_token);
        return this.http.post(ATTEND_EVENT_URL, { 'appointment_id': appointment_id }, { 'headers': token_header }).toPromise().then((res) => {
            console.log(res);
            if (!res.success) {
                return Object(__WEBPACK_IMPORTED_MODULE_2_q__["reject"])(res.message);
            }
            return res;
        });
    }
    my(auth_token) {
        const token_header = new __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["c" /* HttpHeaders */]().set('Authorization', 'Token ' + auth_token);
        return this.http.get(MY_EVENTS_URL, { 'headers': token_header }).toPromise().then((res) => {
            if (!res.success) {
                return Object(__WEBPACK_IMPORTED_MODULE_2_q__["reject"])(res.message);
            }
            this.myAppointments = res;
            console.log('my appointments');
            console.log(res);
            return res;
        });
    }
    invitations(auth_token) {
        // "Public" is a reserved word, so we go with the term "Everyone"
        const token_header = new __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["c" /* HttpHeaders */]().set('Authorization', 'Token ' + auth_token);
        return this.http.get(INVITATEDTO_URL, { 'headers': token_header }).toPromise().then((res) => {
            if (!res.success) {
                return Object(__WEBPACK_IMPORTED_MODULE_2_q__["reject"])(res.message);
            }
            console.log('my invitations');
            console.log(res);
            this.myInvitations = res;
            return res;
        });
    }
    everyone(auth_token) {
        // "Public" is a reserved word, so we go with the term "Everyone"
        const token_header = new __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["c" /* HttpHeaders */]().set('Authorization', 'Token ' + auth_token);
        return this.http.get(PUBLIC_EVENTS_URL, { 'headers': token_header }).toPromise().then((res) => {
            if (!res.success) {
                return Object(__WEBPACK_IMPORTED_MODULE_2_q__["reject"])(res.message);
            }
            console.log('public appointments');
            console.log(res);
            this.everyoneAppointments = res;
            return res;
        });
    }
};
AppointmentService = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["B" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["a" /* HttpClient */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["a" /* HttpClient */]) === "function" && _a || Object])
], AppointmentService);

var _a;
//# sourceMappingURL=appointment.service.js.map

/***/ }),

/***/ "../../../../../src/app/auth.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AuthService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_common_http__ = __webpack_require__("../../../common/@angular/common/http.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_q__ = __webpack_require__("../../../../q/q.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_q___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_q__);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



// TODO
const INTRODUCTION_URL = 'http://localhost:8000/api/introduce/';
const ENROLLMENT_URL = 'http://localhost:8000/api/enroll/';
//  Done
const LOGIN_URL = 'http://localhost:8000/api-token-auth/';
const LOGOUT_URL = 'http://localhost:8000/logout/';
const GET_PROFILE_URL = 'http://localhost:8000/api/my-profile/';
const PROFILE_UPDATE_URL = 'http://localhost:8000/api/update-profile/';
let AuthService = class AuthService {
    constructor(http) {
        this.http = http;
    }
    blank_login() {
        this.login = {
            'email': '',
            'password': '',
            'submitted': false,
            'error_messages': [],
            'success': false
        };
    }
    blank_introduction() {
        this.introduction = {
            'email': '',
            'introduction_code': '',
            'submitted': false,
            'message': ''
        };
    }
    blank_enrollment() {
        this.enrollment = {
            'submitted': false,
            'error_messages': [],
            'success': false
        };
    }
    clear() {
        this.blank_login();
        this.blank_introduction();
        this.blank_enrollment();
    }
    is_selected_location(location_id) {
        for (const l of this.profile.profile.locations) {
            console.log('Comparing ' + location_id + ' to ' + l.id);
            if (l.id === location_id) {
                console.log('match found');
                return true;
            }
        }
        return false;
    }
    send_introduction(introduction_post_data) {
        // Ensure logged in.
        // Add API to backend
        // Ensure this is checked when someone enrolls.
        // Only Salesforce.com emails are acceptable
        const token_header = new __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["c" /* HttpHeaders */]().set('Authorization', 'Token ' + this.token);
        this.introduction.submitted = true;
        this.login.submitted = true;
        this.introduction.email = introduction_post_data.introductionEmail;
        return this.http.post(INTRODUCTION_URL, introduction_post_data, { 'headers': token_header }).toPromise().then((res) => {
            if (!res.success) {
                this.introduction.message = res.message;
                return Object(__WEBPACK_IMPORTED_MODULE_2_q__["reject"])(res.message);
            }
            this.introduction.introduction_code = res.introduction_code;
            this.introduction.email = res.email;
            this.introduction.message = '';
        });
    }
    // Moving to using Login API etc
    send_enrollment(enrollment_post_data) {
        // Anyone can enroll, given that they have a valid api code.
        this.enrollment.submitted = true;
        return this.http.post(ENROLLMENT_URL, enrollment_post_data).toPromise().then((res) => {
            console.log(res);
            if (!res.success) {
                this.enrollment.success = false;
                this.enrollment.error_messages = [res.message];
                return Object(__WEBPACK_IMPORTED_MODULE_2_q__["reject"])(res.message);
            }
            this.enrollment.success = true;
        });
    }
    send_profile_change() {
        const token_header = new __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["c" /* HttpHeaders */]().set('Authorization', 'Token ' + this.token);
        return this.http.post(PROFILE_UPDATE_URL, this.profile, { 'headers': token_header }).toPromise().then((res) => {
            this.profile.updated = res.success;
            if (!res.success) {
                this.profile.updated = true;
                this.profile.message = res.message;
                return Object(__WEBPACK_IMPORTED_MODULE_2_q__["reject"])(res.message);
            }
            setTimeout(() => { this.profile.updated = false; }, 1000);
        });
    }
    my_profile() {
        const token_header = new __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["c" /* HttpHeaders */]().set('Authorization', 'Token ' + this.token);
        return this.http.get(GET_PROFILE_URL, { 'headers': token_header }).toPromise().then((res) => {
            if (!res.success) {
                this.login.error_messages = [res.message];
                return Object(__WEBPACK_IMPORTED_MODULE_2_q__["reject"])('Login failed.  Please check your email and password');
            }
            this.profile = res;
            this.profile.updated = false;
            console.log('setting profile');
            console.log(this.profile);
            this.login.success = true;
            return res;
        });
    }
    send_login(login_data) {
        this.login.submitted = true;
        const prom = this.http.post(LOGIN_URL, {
            'username': login_data.loginFormEmail,
            'password': login_data.loginFormPassword
        }).toPromise();
        this.login.password = ''; // Delete the login password after we submit.
        return prom.then((res) => {
            console.log('login api response');
            console.log(res);
            this.token = res.token;
        });
    }
    check_cookies(cookieService) {
        const token = cookieService.get('login_token');
        if (token) {
            this.token = token;
            return true;
        }
        return false;
    }
    logout(cookieService) {
        const token_header = new __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["c" /* HttpHeaders */]().set('Authorization', 'Token ' + this.token);
        return this.http.get(LOGOUT_URL, { 'headers': token_header }).toPromise().then((res) => {
            if (!res.success) {
                return Object(__WEBPACK_IMPORTED_MODULE_2_q__["reject"])('Failure while logging out.');
            }
            cookieService.deleteAll();
            this.clear();
            return res;
        });
    }
};
AuthService = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["B" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["a" /* HttpClient */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["a" /* HttpClient */]) === "function" && _a || Object])
], AuthService);

var _a;
//# sourceMappingURL=auth.service.js.map

/***/ }),

/***/ "../../../../../src/app/availability/availability.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, ".past, li.list-group-item.previousmonth.past {\n  background-color: dimgray;\n}\n\n.previousmonth {\n  background-color: lightgoldenrodyellow;\n}\n\n.nextmonth {\n  background-color: lightgoldenrodyellow;\n}\n\n.selected {\n  background-color: greenyellow !important ;\n}\n\n@media (min-width: 768px){\n  .seven-cols .col-md-1,\n  .seven-cols .col-sm-1,\n  .seven-cols .col-lg-1  {\n    width: 14.285714285714285714285714285714%;\n    *width: 14.285714285714285714285714285714%;\n  }\n}\n\n@media (min-width: 992px) {\n  .seven-cols .col-md-1,\n  .seven-cols .col-sm-1,\n  .seven-cols .col-lg-1 {\n    width: 14.285714285714285714285714285714%;\n    *width: 14.285714285714285714285714285714%;\n  }\n}\n\n/**\n *  The following is not really needed in this case\n *  Only to demonstrate the usage of @media for large screens\n */\n@media (min-width: 1200px) {\n  .seven-cols .col-md-1,\n  .seven-cols .col-sm-1,\n  .seven-cols .col-lg-1 {\n    width: 14.285714285714285714285714285714%;\n    *width: 14.285714285714285714285714285714%;\n  }\n}\n", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/availability/availability.component.html":
/***/ (function(module, exports) {

module.exports = "<p>Availability Calendar</p>\n\n<div class=\"row\">\n  <div class=\"col-sm-6\">\n\n    <div class=\"input-group\">\n      <div class=\"input-group-btn\">\n        <button type=\"button\" class=\"btn btn-default\" (click)=\"prev_month()\"><span class=\"glyphicon glyphicon-chevron-left\"></span> Prev</button>\n      </div>\n      <input type=\"text\" class=\"form-control\" aria-label=\"...\" value=\"{{ current.getFullYear() }} - {{ current.toLocaleString('ja-jp', { month: 'long' }) }}\" disabled>\n\n      <div class=\"input-group-btn\">\n        <button type=\"button\" class=\"btn btn-default\" (click)=\"next_month()\">Next <span class=\"glyphicon glyphicon-chevron-right\"></span></button>\n      </div>\n    </div>\n    <div class=\"row seven-cols hidden-xs\">\n      <div class=\"col-sm-1\">月</div>\n      <div class=\"col-sm-1\">火</div>\n      <div class=\"col-sm-1\">水</div>\n      <div class=\"col-sm-1\">木</div>\n      <div class=\"col-sm-1\">金</div>\n      <div class=\"col-sm-1\">土</div>\n      <div class=\"col-sm-1\">日</div>\n      <hr>\n      <div class=\"col-sm-1\" *ngFor=\"let d of display_dates\" [ngClass]=\"{'past': d < today,\n                  'nextmonth': d.getMonth() > current.getMonth(),\n                  'previousmonth': d.getMonth() < current.getMonth(),\n                  'selected':  is_selected_date(d)}\" (click)=\"toggle_date(d)\">{{ d | date:'dd' }}　</div>\n    </div>\n\n\n    <ul class=\"list-group hidden-sm hidden-md hidden-lg\">\n      <li class=\"list-group-item\" *ngFor=\"let d of display_dates\"\n      [ngClass]=\"{'past': d < today,\n                  'nextmonth': d.getMonth() > current.getMonth(),\n                  'previousmonth': d.getMonth() < current.getMonth(),\n                  'selected':  is_selected_date(d),\n                  'list-group-item-success':  d < today && is_selected_date(d),\n                  'list-group-item-info': d > today && is_selected_date(d)}\"\n      (click)=\"toggle_date(d)\">\n                  {{ d | date:'yyyy-MM-dd' }}\n                  ({{ d.toLocaleString('ja-jp', { weekday: 'short' }) }})\n      </li>\n    </ul>\n\n    <button type=\"button\" class=\"btn btn-default\" (click)=\"submitAvailability()\">Update my Availability</button>\n  </div>\n  <div class=\"col-sm-6\">\n    Your next 5 days are:\n    <ul>\n      <li class=\"list-group-item\" *ngFor=\"let d of selected_dates_array\">\n        {{ d | date: 'yyyy-MM-dd'}}\n      </li>\n    </ul>\n  </div>\n</div>\n"

/***/ }),

/***/ "../../../../../src/app/availability/availability.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return AvailabilityComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__appointment_service__ = __webpack_require__("../../../../../src/app/appointment.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__auth_service__ = __webpack_require__("../../../../../src/app/auth.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



function getWeekNumber(d) {
    // Copy date so don't modify original
    d = new Date(Date.UTC(d.getFullYear(), d.getMonth(), d.getDate()));
    // Set to nearest Thursday: current date + 4 - current day number
    // Make Sunday's day number 7
    d.setUTCDate(d.getUTCDate() + 7 - (d.getUTCDay() || 7));
    // Get first day of year
    const yearStart = new Date(Date.UTC(d.getUTCFullYear(), 0, 1));
    // Calculate full weeks to nearest Thursday
    const weekNo = Math.ceil((((d.getTime() - yearStart.getTime()) / 86400000) + 1) / 7);
    // Return array of year and week number
    return [d.getUTCFullYear(), weekNo];
}
let AvailabilityComponent = class AvailabilityComponent {
    constructor(appointmentService, authService) {
        this.appointmentService = appointmentService;
        this.authService = authService;
        this.selected_dates = {};
        this.selected_dates_array = [];
        this.display_dates = [];
    }
    reset() {
        this.today = new Date();
        this.current = new Date(this.today);
    }
    clear() {
        this.selected_dates = {};
        this.selected_dates_array = [];
    }
    set_availability() {
        for (const avail of this.appointmentService.myAvailability.availability) {
            this.toggle_date(avail.date);
        }
    }
    submitAvailability() {
        console.log('Submitting availability to server');
        console.log(this.selected_dates);
        this.appointmentService.send_availability(this.authService.token, this.current.getMonth() + 1, Object.keys(this.selected_dates)).then((res) => {
            this.clear();
            this.set_availability();
            return res;
        }).then((res) => {
            // TODO: Show error messages for places you couldn't change availability
            // IE: Places you have already inserted appointments
            console.log(res);
            return res;
        }).catch((err) => {
            console.log(err);
        });
    }
    // Get all days for this month; includes days to round out the week, and removes any old days before the start of the current week,
    // since there is no point (yet) in showing them.
    getDaysInMonth(month, year) {
        const lastweek = new Date(year, month, 1);
        lastweek.setDate(lastweek.getDate() - 6);
        const d = new Date(year, month, 1);
        const days = [];
        while (lastweek.getMonth() < month) {
            if (getWeekNumber(lastweek)[1] === getWeekNumber(d)[1] && getWeekNumber(d) >= getWeekNumber(this.today)) {
                days.push(new Date(lastweek));
            }
            lastweek.setDate(lastweek.getDate() + 1);
        }
        while (d.getMonth() === month) {
            if (getWeekNumber(d) >= getWeekNumber(this.today)) {
                days.push(new Date(d));
            }
            d.setDate(d.getDate() + 1);
        }
        while (getWeekNumber(d)[1] === getWeekNumber(this.today)[1]) {
            days.push(new Date(d));
            d.setDate(d.getDate() + 1);
        }
        return days;
    }
    ngOnInit() {
        this.clear();
        this.reset();
        this.set_availability();
        this.set_display_dates();
    }
    date_str(d) {
        return d.getFullYear() + '-' + (d.getMonth() + 1) + '-' + d.getDate();
    }
    toggle_date(d) {
        // Returns true if it is selected now, or false if it is not.
        // const k = d.toISOString().split('T')[0];
        const k = this.date_str(d);
        const add_date = d > this.today && !this.selected_dates[k];
        if (add_date) {
            this.selected_dates[k] = d;
        }
        else {
            delete (this.selected_dates[k]);
        }
        this.set_selected_dates();
        return this.selected_dates[this.date_str(d)];
    }
    is_selected_date(d) {
        return this.selected_dates[this.date_str(d)];
    }
    set_display_dates() {
        this.display_dates = this.getDaysInMonth(this.current.getMonth(), this.current.getFullYear());
    }
    set_selected_dates() {
        const ret = Object.keys(this.selected_dates);
        const to_sort = [];
        for (const b of ret) {
            const c = new Date(b);
            to_sort.push(c);
        }
        to_sort.sort((a, b) => {
            return a - b;
        });
        this.selected_dates_array = to_sort.slice(0, 5);
    }
    next_month() {
        this.current.setMonth(this.current.getMonth() + 1);
        this.set_display_dates();
    }
    prev_month() {
        this.current.setMonth(this.current.getMonth() - 1);
        if ((this.current.getFullYear() === this.today.getFullYear() && this.current.getMonth() < this.today.getMonth()) ||
            (this.current.getFullYear() < this.today.getFullYear())) {
            this.current = Object.assign(new Date(), this.today);
            return;
        }
        this.set_display_dates();
    }
};
AvailabilityComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
        selector: 'app-availability',
        changeDetection: __WEBPACK_IMPORTED_MODULE_0__angular_core__["j" /* ChangeDetectionStrategy */].OnPush,
        template: __webpack_require__("../../../../../src/app/availability/availability.component.html"),
        styles: [__webpack_require__("../../../../../src/app/availability/availability.component.css")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__appointment_service__["a" /* AppointmentService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__appointment_service__["a" /* AppointmentService */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_2__auth_service__["a" /* AuthService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__auth_service__["a" /* AuthService */]) === "function" && _b || Object])
], AvailabilityComponent);

var _a, _b;
//# sourceMappingURL=availability.component.js.map

/***/ }),

/***/ "../../../../../src/app/enrollment/enrollment.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/enrollment/enrollment.component.html":
/***/ (function(module, exports) {

module.exports = "<form id=\"enrollmentForm\" (ngSubmit)=\"onSubmitEnrollment();\" #enrollmentForm=\"ngForm\">\n    <h2>Enrollment: </h2>\n      <!-- Create an account, select a place. -->\n    <div class=\"alert alert-danger\" role=\"alert\" [hidden]=\"authService.enrollment.error_messages.length == 0\">\n      <span class=\"glyphicon glyphicon-exclamation-sign\" aria-hidden=\"true\"></span>\n      <span class=\"sr-only\">Error:</span>\n      <span *ngFor=\"let err_msg of authService.enrollment.error_messages\">\n          {{err_msg}}<br>\n      </span>\n    </div>\n\n    <div class=\"form-group\">\n      <label for=\"enrollmentEmail\">Email address</label>\n      <input type=\"email\" class=\"form-control\" id=\"enrollmentEmail\" name=\"enrollmentEmail\" placeholder=\"Email@example.org\"\n             ngModel required #enrollmentEmail=\"ngModel\" email=\"true\" appSalesforceOnly>\n      <div [hidden]=\"enrollmentEmail.valid || enrollmentEmail.pristine && !authService.enrollment.submitted\"\n           class=\"alert alert-danger\">\n        You must enter a valid email.  You can only register with a salesforce.com email.\n      </div>\n    </div>\n\n    <div class=\"form-group\">\n      <label for=\"enrollmentPassword\">Password</label>\n      <input type=\"password\" class=\"form-control\" id=\"enrollmentPassword\" name=\"enrollmentPassword\"\n             placeholder=\"Password\"\n             ngModel minlength=\"8\" #enrollmentPassword=\"ngModel\"\n             required>\n      <div [hidden]=\"enrollmentPassword.valid || enrollmentPassword.pristine\"\n           class=\"alert alert-danger\">\n        You must enter a password of more than 8 characters.\n      </div>\n    </div>\n\n    <div class=\"form-group\">\n      <label for=\"enrollmentIntroductionCode\">Introduction Code</label>\n      <input type=\"text\" class=\"form-control\" id=\"enrollmentIntroductionCode\" name=\"enrollmentIntroductionCode\"\n             placeholder=\"abc-123\" ngModel required>\n      <div [hidden]=\"enrollmentPassword.valid\"\n           class=\"alert alert-warning\">\n        You cannot enroll without an introduction code\n      </div>\n    </div>\n\n    <div class=\"form-group\">\n      <label for=\"selectWhitelist\">I like</label>\n      <select multiple=\"multiple\" id=\"selectWhitelist\" name=\"selectWhitelist\" class=\"form-control\"\n              ngModel [compareWith]=\"compareIdFn\">\n        <option *ngFor=\"let foodOption of foodOptions\" [ngValue]=\"foodOption\">{{foodOption.name}}</option>\n      </select>\n    </div>\n\n    <div class=\"form-group\">\n      <label for=\"selectLocation\">I can meet you near</label>\n      <select multiple=\"multiple\" id=\"selectLocation\" name=\"selectLocation\" class=\"form-control\"\n              ngModel [compareWith]=\"compareIdFn\">\n        <option *ngFor=\"let locationOption of locationOptions\" [ngValue]=\"locationOption\">{{locationOption.name}}</option>\n      </select>\n    </div>\n\n    <button class=\"btn btn-default\">Submit</button>\n  </form>\n"

/***/ }),

/***/ "../../../../../src/app/enrollment/enrollment.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return EnrollmentComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__auth_service__ = __webpack_require__("../../../../../src/app/auth.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__nav_service__ = __webpack_require__("../../../../../src/app/nav.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__angular_forms__ = __webpack_require__("../../../forms/@angular/forms.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};




let EnrollmentComponent = class EnrollmentComponent {
    constructor(navService, authService) {
        this.navService = navService;
        this.authService = authService;
    }
    compareIdFn(l1, l2) {
        return l1.id === l2.id;
    }
    onSubmitEnrollment() {
        // Ensure validity of form
        this.navService.waiting();
        this.authService.send_enrollment(this.enrollmentForm.value).then(() => {
            this.navService.login();
        }).catch(() => {
            this.navService.enrollment();
        });
    }
    ngOnInit() {
    }
};
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_13" /* ViewChild */])('enrollmentForm'),
    __metadata("design:type", typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_3__angular_forms__["e" /* NgForm */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__angular_forms__["e" /* NgForm */]) === "function" && _a || Object)
], EnrollmentComponent.prototype, "enrollmentForm", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["E" /* Input */])(),
    __metadata("design:type", Array)
], EnrollmentComponent.prototype, "foodOptions", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["E" /* Input */])(),
    __metadata("design:type", Array)
], EnrollmentComponent.prototype, "locationOptions", void 0);
EnrollmentComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
        selector: 'app-enrollment',
        template: __webpack_require__("../../../../../src/app/enrollment/enrollment.component.html"),
        styles: [__webpack_require__("../../../../../src/app/enrollment/enrollment.component.css")]
    }),
    __metadata("design:paramtypes", [typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_2__nav_service__["a" /* NavService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__nav_service__["a" /* NavService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_1__auth_service__["a" /* AuthService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__auth_service__["a" /* AuthService */]) === "function" && _c || Object])
], EnrollmentComponent);

var _a, _b, _c;
//# sourceMappingURL=enrollment.component.js.map

/***/ }),

/***/ "../../../../../src/app/init.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return InitService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_common_http__ = __webpack_require__("../../../common/@angular/common/http.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_q__ = __webpack_require__("../../../../q/q.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2_q___default = __webpack_require__.n(__WEBPACK_IMPORTED_MODULE_2_q__);
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



const FOODOPTIONS_URL = 'http://localhost:8000/api/food-options/';
const LOCATIONS_URL = 'http://localhost:8000/api/locations/';
let InitService = class InitService {
    constructor(http) {
        this.http = http;
    }
    // Moving to using Login API etc
    food_options() {
        return this.http.get(FOODOPTIONS_URL).toPromise().then((res) => {
            if (!res.success) {
                return Object(__WEBPACK_IMPORTED_MODULE_2_q__["reject"])(res.message);
            }
            return res;
        });
    }
    // Moving to using Login API etc
    locations() {
        return this.http.get(LOCATIONS_URL).toPromise().then((res) => {
            if (!res.success) {
                return Object(__WEBPACK_IMPORTED_MODULE_2_q__["reject"])(res.message);
            }
            return res;
        });
    }
};
InitService = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["B" /* Injectable */])(),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["a" /* HttpClient */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__angular_common_http__["a" /* HttpClient */]) === "function" && _a || Object])
], InitService);

var _a;
//# sourceMappingURL=init.service.js.map

/***/ }),

/***/ "../../../../../src/app/introduction/introduction.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/introduction/introduction.component.html":
/***/ (function(module, exports) {

module.exports = "<div class=\"alert alert-danger\" role=\"alert\" [hidden]=\"!authService.introduction.message\">\n  <span class=\"glyphicon glyphicon-exclamation-sign\" aria-hidden=\"true\"></span>\n  <span class=\"sr-only\">Error:</span>\n  {{authService.introduction.message}}\n</div>\n\n<form id=\"introductionForm\" (ngSubmit)=\"onSubmitIntroduction()\" #introductionForm=\"ngForm\">\n  <div class=\"form-group\">\n    <label for=\"InvitationEmail\">Who do you want to introduce?</label>\n    <input type=\"email\" class=\"form-control\" id=\"InvitationEmail\" name=\"invitationEmail\" placeholder=\"Email@example.org\"\n           ngModel required #invitationEmail=\"ngModel\"  email=\"true\" appSalesforceOnly>\n      <div [hidden]=\"invitationEmail.valid || invitationEmail.pristine\" class=\"alert alert-danger\">\n        You must enter a valid email.  You can only register with a salesforce.com email.\n      </div>\n\n  </div>\n  <button type=\"submit\" class=\"btn btn-default\" [disabled]=\"!invitationEmail.valid || invitationEmail.pristine\">Submit</button>\n</form>\n"

/***/ }),

/***/ "../../../../../src/app/introduction/introduction.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return IntroductionComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__appointment_service__ = __webpack_require__("../../../../../src/app/appointment.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__auth_service__ = __webpack_require__("../../../../../src/app/auth.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__angular_forms__ = __webpack_require__("../../../forms/@angular/forms.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__nav_service__ = __webpack_require__("../../../../../src/app/nav.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};





let IntroductionComponent = class IntroductionComponent {
    constructor(appointmentService, authService, navService) {
        this.appointmentService = appointmentService;
        this.authService = authService;
        this.navService = navService;
    }
    ngOnInit() {
    }
    onSubmitIntroduction() {
        this.navService.waiting();
        console.log('waiting');
        this.authService.send_introduction(this.introductionForm.value).then(() => {
            this.navService.introductionsuccess();
            console.log('success');
        }).catch(() => {
            this.navService.introduction();
            console.log('failure');
        });
    }
};
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_13" /* ViewChild */])('introductionForm'),
    __metadata("design:type", typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_3__angular_forms__["e" /* NgForm */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__angular_forms__["e" /* NgForm */]) === "function" && _a || Object)
], IntroductionComponent.prototype, "introductionForm", void 0);
IntroductionComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
        selector: 'app-introduction',
        template: __webpack_require__("../../../../../src/app/introduction/introduction.component.html"),
        styles: [__webpack_require__("../../../../../src/app/introduction/introduction.component.css")]
    }),
    __metadata("design:paramtypes", [typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_1__appointment_service__["a" /* AppointmentService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__appointment_service__["a" /* AppointmentService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_2__auth_service__["a" /* AuthService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__auth_service__["a" /* AuthService */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_4__nav_service__["a" /* NavService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4__nav_service__["a" /* NavService */]) === "function" && _d || Object])
], IntroductionComponent);

var _a, _b, _c, _d;
//# sourceMappingURL=introduction.component.js.map

/***/ }),

/***/ "../../../../../src/app/invitation-success/invitation-success.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/invitation-success/invitation-success.component.html":
/***/ (function(module, exports) {

module.exports = "<p>You successfully submitted a request for an invitation code. <a href=\"#\" (click)=\"goInvitation()\">Make another request?</a></p>\n<div class=\"form-group\">\n    <label for=\"InvitationEmailOutput\">Invitee</label>\n    <input type=\"email\" class=\"form-control\" id=\"InvitationEmailOutput\" name=\"InvitationEmailOutput\" [(ngModel)]=\"authService.introduction.email\" disabled>\n</div>\n<div class=\"form-group\">\n    <label for=\"InvitationCodeOutput\">Introduction Code</label>\n    <input type=\"text\" class=\"form-control\" id=\"InvitationCodeOutput\" name=\"InvitationCodeOutput\" [(ngModel)]=\"authService.introduction.introduction_code\" disabled>\n</div>\n"

/***/ }),

/***/ "../../../../../src/app/invitation-success/invitation-success.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return InvitationSuccessComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__nav_service__ = __webpack_require__("../../../../../src/app/nav.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__auth_service__ = __webpack_require__("../../../../../src/app/auth.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};



let InvitationSuccessComponent = class InvitationSuccessComponent {
    constructor(authService, navService) {
        this.authService = authService;
        this.navService = navService;
    }
    ngOnInit() {
    }
    goInvitation() {
        this.authService.blank_introduction();
        this.navService.introduction();
    }
};
InvitationSuccessComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
        selector: 'app-invitation-success',
        template: __webpack_require__("../../../../../src/app/invitation-success/invitation-success.component.html"),
        styles: [__webpack_require__("../../../../../src/app/invitation-success/invitation-success.component.css")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_2__auth_service__["a" /* AuthService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__auth_service__["a" /* AuthService */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_1__nav_service__["a" /* NavService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__nav_service__["a" /* NavService */]) === "function" && _b || Object])
], InvitationSuccessComponent);

var _a, _b;
//# sourceMappingURL=invitation-success.component.js.map

/***/ }),

/***/ "../../../../../src/app/login/login.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/login/login.component.html":
/***/ (function(module, exports) {

module.exports = "<div class=\"col-sm-6\">\n  <form id=\"loginForm\" (submit)=\"onSubmitLogin()\" #loginForm=\"ngForm\">\n\n    <div class=\"alert alert-danger\" role=\"alert\" [hidden]=\"authService.login.error_messages.length == 0\">\n      <span class=\"glyphicon glyphicon-exclamation-sign\" aria-hidden=\"true\"></span>\n      <span class=\"sr-only\">Error:</span>\n      <span *ngFor=\"let err_msg of authService.login.error_messages\">\n          {{err_msg}}<br>\n      </span>\n    </div>\n    <div class=\"alert alert-success\" role=\"alert\" [hidden]=\"!authService.enrollment.submitted || !authService.enrollment.success\">\n      <span class=\"glyphicon glyphicon-check\" aria-hidden=\"true\"></span>\n      Your Enrollment was successful.  Please log in using the same email and password.\n    </div>\n  <p>Please login:</p>\n  <div class=\"form-group\">\n    <label for=\"loginFormEmail\">Email address</label>\n    <input type=\"email\" class=\"form-control\" id=\"loginFormEmail\" name=\"loginFormEmail\"\n           placeholder=\"Email\" ngModel #loginFormEmail=\"ngModel\" email=\"true\" required appSalesforceOnly>\n  </div>\n\n  <div class=\"form-group\">\n    <label for=\"loginFormPassword\">Password</label>\n    <input type=\"password\" class=\"form-control\" id=\"loginFormPassword\" name=\"loginFormPassword\"\n             placeholder=\"Password\" ngModel minlength=\"8\" #loginFormPassword=\"ngModel\"\n             required>\n  </div>\n  <button class=\"btn btn-default\">Submit</button>\n</form>\n</div>\n<div class=\"col-sm-6\">\n  <h2>LunchCloud</h2>\n  <p>Find people and eat lunch with them.</p>\n</div>\n"

/***/ }),

/***/ "../../../../../src/app/login/login.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return LoginComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__nav_service__ = __webpack_require__("../../../../../src/app/nav.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__auth_service__ = __webpack_require__("../../../../../src/app/auth.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__appointment_service__ = __webpack_require__("../../../../../src/app/appointment.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__angular_forms__ = __webpack_require__("../../../forms/@angular/forms.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};





let LoginComponent = class LoginComponent {
    constructor(authService, navService, appointmentService) {
        this.authService = authService;
        this.navService = navService;
        this.appointmentService = appointmentService;
        this.loginEvent = new __WEBPACK_IMPORTED_MODULE_0__angular_core__["w" /* EventEmitter */]();
    }
    ngOnInit() {
    }
    onSubmitLogin() {
        // We need to load our own events, and the public / 'Everyone' appointments
        this.navService.waiting();
        console.log(this.loginEvent.emit(this.loginForm.value));
    }
};
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_13" /* ViewChild */])('loginForm'),
    __metadata("design:type", typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_4__angular_forms__["e" /* NgForm */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4__angular_forms__["e" /* NgForm */]) === "function" && _a || Object)
], LoginComponent.prototype, "loginForm", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["R" /* Output */])(),
    __metadata("design:type", Object)
], LoginComponent.prototype, "loginEvent", void 0);
LoginComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
        selector: 'app-login',
        template: __webpack_require__("../../../../../src/app/login/login.component.html"),
        styles: [__webpack_require__("../../../../../src/app/login/login.component.css")]
    }),
    __metadata("design:paramtypes", [typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_2__auth_service__["a" /* AuthService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__auth_service__["a" /* AuthService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_1__nav_service__["a" /* NavService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__nav_service__["a" /* NavService */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_3__appointment_service__["a" /* AppointmentService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__appointment_service__["a" /* AppointmentService */]) === "function" && _d || Object])
], LoginComponent);

var _a, _b, _c, _d;
//# sourceMappingURL=login.component.js.map

/***/ }),

/***/ "../../../../../src/app/my-events/my-events.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/my-events/my-events.component.html":
/***/ (function(module, exports) {

module.exports = "<div class=\"alert alert-success\" role=\"alert\" [hidden]=\"!joinedAppointment\">\n  <span class=\"glyphicon glyphicon-check\" aria-hidden=\"true\"></span>\n  <span class=\"sr-only\">Successfully joined:</span>\n  You successfully joined the event (xxx)\n</div>\n\n<strong>My Upcoming Lunches: </strong>\n\n<app-appointment-item [appointments]=\"appointmentService.myAppointments.appointments\" [allowJoiningEvent]=false *ngIf=\"appointmentService.myAppointments && appointmentService.myAppointments.appointments.length > 0\"></app-appointment-item>\n<div *ngIf=\"appointmentService.myAppointments.appointments.length == 0\">\n  <h2>You have no lunches!</h2>\n  <ol class=\"list-group\">\n    <li class=\"list-group-item\" (click)=\"goPublicEvents()\"><a href=\"#\"><span class=\"glyphicon glyphicon-calendar\"></span> Find upcoming lunches near you?</a></li>\n    <li class=\"list-group-item\" (click)=\"goAvailability()\"><a href=\"#\"><span class=\"glyphicon glyphicon-time\"></span> Add availability for lunch?</a></li>\n  </ol>\n</div>\n"

/***/ }),

/***/ "../../../../../src/app/my-events/my-events.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return MyEventsComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__appointment_service__ = __webpack_require__("../../../../../src/app/appointment.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__auth_service__ = __webpack_require__("../../../../../src/app/auth.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__nav_service__ = __webpack_require__("../../../../../src/app/nav.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};




let MyEventsComponent = class MyEventsComponent {
    constructor(appointmentService, authService, navService) {
        this.appointmentService = appointmentService;
        this.authService = authService;
        this.navService = navService;
    }
    goAvailability() {
        this.navService.availability();
    }
    goPublicEvents() {
        this.navService.publicevents();
    }
    ngOnInit() {
    }
};
MyEventsComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
        selector: 'app-my-events',
        template: __webpack_require__("../../../../../src/app/my-events/my-events.component.html"),
        styles: [__webpack_require__("../../../../../src/app/my-events/my-events.component.css")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__appointment_service__["a" /* AppointmentService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__appointment_service__["a" /* AppointmentService */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_2__auth_service__["a" /* AuthService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__auth_service__["a" /* AuthService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_3__nav_service__["a" /* NavService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__nav_service__["a" /* NavService */]) === "function" && _c || Object])
], MyEventsComponent);

var _a, _b, _c;
//# sourceMappingURL=my-events.component.js.map

/***/ }),

/***/ "../../../../../src/app/my-profile/my-profile.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/my-profile/my-profile.component.html":
/***/ (function(module, exports) {

module.exports = "<form id=\"profileForm\" (submit)=\"onSubmitProfileForm();\">\n    <h2>Profile: </h2>\n\n    <div class=\"alert alert-success\" role=\"alert\" [hidden]=\"!authService.profile.updated\">\n      <span class=\"glyphicon glyphicon-check\" aria-hidden=\"true\"></span>\n      <span class=\"sr-only\">Error:</span>\n      Profile update completed.\n    </div>\n\n    <div class=\"alert alert-danger\" role=\"alert\" [hidden]=\"!authService.profile.message\">\n      <span class=\"glyphicon glyphicon-exclamation-sign\" aria-hidden=\"true\"></span>\n      <span class=\"sr-only\">Error:</span>\n      <span>\n          {{authService.profile.message}}<br>\n      </span>\n    </div>\n\n    <div class=\"form-group\">\n      <label for=\"profileEmail\">Email address</label>\n      <input type=\"email\" class=\"form-control\" id=\"profileEmail\" name=\"profileEmail\" placeholder=\"Email\"\n             [(ngModel)]=\"authService.profile.profile.email\" disabled>\n    </div>\n\n    <div class=\"form-group\">\n      <label for=\"profileWhiteList\">I like</label>\n      <select multiple=\"multiple\" id=\"profileWhiteList\" name=\"profileWhiteList\" class=\"form-control\"\n              [(ngModel)]=\"authService.profile.profile.whitelist\"  [compareWith]=\"compareIdFn\">\n        <option *ngFor=\"let foodOption of foodOptions\" id=\"profile_{{foodOption.id}}\" [ngValue]=\"foodOption\">{{foodOption.name}}</option>\n      </select>\n    </div>\n\n    <div class=\"form-group\">\n      <label for=\"profileLocation\">I can meet you near</label>\n      <select multiple=\"multiple\" id=\"profileLocation\" name=\"profileLocation\" class=\"form-control\"\n              [(ngModel)]=\"authService.profile.profile.locations\" [compareWith]=\"compareIdFn\">\n        <option *ngFor=\"let locationOption of locationOptions\" id=\"profile_{{locationOption.id}}\" [ngValue]=\"locationOption\">{{locationOption.name}}</option>\n      </select>\n    </div>\n\n\n    <button class=\"btn btn-default\">Submit</button>\n  </form>\n"

/***/ }),

/***/ "../../../../../src/app/my-profile/my-profile.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return MyProfileComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__auth_service__ = __webpack_require__("../../../../../src/app/auth.service.ts");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


let MyProfileComponent = class MyProfileComponent {
    constructor(authService) {
        this.authService = authService;
    }
    compareIdFn(l1, l2) {
        return l1.id === l2.id;
    }
    onSubmitProfileForm() {
        this.authService.send_profile_change().catch((err) => {
            console.log(err);
        });
    }
    ngOnInit() {
    }
};
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["E" /* Input */])(),
    __metadata("design:type", Array)
], MyProfileComponent.prototype, "foodOptions", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["E" /* Input */])(),
    __metadata("design:type", Array)
], MyProfileComponent.prototype, "locationOptions", void 0);
MyProfileComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
        selector: 'app-my-profile',
        template: __webpack_require__("../../../../../src/app/my-profile/my-profile.component.html"),
        styles: [__webpack_require__("../../../../../src/app/my-profile/my-profile.component.css")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__auth_service__["a" /* AuthService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__auth_service__["a" /* AuthService */]) === "function" && _a || Object])
], MyProfileComponent);

var _a;
//# sourceMappingURL=my-profile.component.js.map

/***/ }),

/***/ "../../../../../src/app/nav.service.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return NavService; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};

let NavService = class NavService {
    constructor() {
        this.state = 'login';
    }
    is(to_check) {
        return this.state === to_check;
    }
    introductionsuccess() {
        this.state = 'introductionsuccess';
    }
    loadmyevents() {
        this.state = 'loadmyevents';
    }
    login() {
        this.state = 'login';
    }
    waiting() {
        this.state = 'waiting';
    }
    introduction() {
        this.state = 'introduction';
    }
    availability() {
        this.state = 'availability';
    }
    search() {
        this.state = 'search';
    }
    publicevents() {
        this.state = 'publicevents';
    }
    invitedto() {
        this.state = 'invitedto';
    }
    myevents() {
        this.state = 'myevents';
    }
    profile() {
        this.state = 'profile';
    }
    enrollment() {
        this.state = 'enrollment';
    }
};
NavService = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["B" /* Injectable */])(),
    __metadata("design:paramtypes", [])
], NavService);

//# sourceMappingURL=nav.service.js.map

/***/ }),

/***/ "../../../../../src/app/nav/nav.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/nav/nav.component.html":
/***/ (function(module, exports) {

module.exports = "<div class=\"container-fluid\">\n  <!-- Brand and toggle get grouped for better mobile display -->\n  <div class=\"navbar-header\">\n    <button type=\"button\" class=\"navbar-toggle collapsed\" data-toggle=\"collapse\" aria-expanded=\"false\">\n      <span class=\"sr-only\">Toggle navigation</span>\n      <span class=\"icon-bar\"></span>\n      <span class=\"icon-bar\"></span>\n      <span class=\"icon-bar\"></span>\n    </button>\n    <a class=\"navbar-brand\" href=\"#\">\n      <img alt=\"LunchForce\" src=\"assets/sandwich-311262_640.png\">\n    </a>\n  </div>\n\n  <!-- Collect the nav links, forms, and other content for toggling -->\n    <ul class=\"nav navbar-nav\" *ngIf=\"!authService.login.success; else WelcomeNav\">\n      <li (click)=\"navService.login()\" [ngClass]=\"{'active': state == 'login'}\"><a href=\"#\">Login <span class=\"sr-only\">(current)</span></a></li>\n      <li (click)=\"navService.enrollment()\" [ngClass]=\"{'active': state == 'enrollment'}\"><a href=\"#\">Enrollment</a></li>\n    </ul>\n    <ng-template #WelcomeNav>\n      <ul class=\"nav navbar-nav\"><li class=\"navbar-text\" >Welcome back {{ authService.profile.profile.name }}</li></ul>\n    </ng-template>\n\n    <ul class=\"nav navbar-nav navbar-right\" *ngIf=\"authService.login.success\">\n      <li [ngClass]=\"{'active': navService.state == 'myevents'}\" (click)=\"navService.myevents()\"><a href=\"#\"><span class=\"glyphicon glyphicon-th-list\"></span> My Events</a></li>\n      <li [ngClass]=\"{'active': navService.state == 'publicevents'}\" (click)=\"navService.publicevents()\"><a href=\"#\"><span class=\"glyphicon glyphicon-calendar\"></span> Public <span class=\"badge\">{{appointmentService.everyoneAppointments.appointments.length}}</span></a></li>\n      <li [ngClass]=\"{'active': navService.state == 'invitedto'}\" (click)=\"navService.invitedto()\"><a href=\"#\"><span class=\"glyphicon glyphicon-calendar\"></span> Invitations <span class=\"badge\">{{appointmentService.myInvitations.appointments.length}}</span></a></li>\n      <li [ngClass]=\"{'active': navService.state == 'availability'}\" (click)=\"navService.availability()\"><a href=\"#\"><span class=\"glyphicon glyphicon-time\"></span> Availability</a></li>\n      <li [ngClass]=\"{'active': navService.state == 'profile'}\" (click)=\"navService.profile()\"><a href=\"#\"><span class=\"glyphicon glyphicon-user\"></span> Profile</a></li>\n      <li [ngClass]=\"{'active': navService.state == 'search'}\" (click)=\"navService.search()\"><a href=\"#\"><span class=\"glyphicon glyphicon-search\"></span> Search</a></li>\n      <li [ngClass]=\"{'active': navService.state == 'introductionsuccess' || navService.state == 'introduction'}\" (click)=\"navService.introduction()\"><a href=\"#\"><span class=\"glyphicon glyphicon-share\"></span> Introduce</a></li>\n      <li [ngClass]=\"{'active': navService.state == 'logout'}\" (click)=\"goLogout()\"><a href=\"#\"><span class=\"glyphicon glyphicon-log-out\"></span> Logout</a></li>\n    </ul>\n</div><!-- /.container-fluid -->\n"

/***/ }),

/***/ "../../../../../src/app/nav/nav.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return NavComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__auth_service__ = __webpack_require__("../../../../../src/app/auth.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__appointment_service__ = __webpack_require__("../../../../../src/app/appointment.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__nav_service__ = __webpack_require__("../../../../../src/app/nav.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4_ngx_cookie_service__ = __webpack_require__("../../../../ngx-cookie-service/index.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};





let NavComponent = class NavComponent {
    constructor(authService, appointmentService, navService, cookieService) {
        this.authService = authService;
        this.appointmentService = appointmentService;
        this.navService = navService;
        this.cookieService = cookieService;
    }
    ngOnInit() {
    }
    goLogout() {
        this.authService.logout(this.cookieService).then(() => {
            console.log('Logout Successful.');
            this.authService.clear();
            this.appointmentService.clear();
            this.navService.login();
        }).catch((err) => {
            console.log(err);
            console.log('failure while logging out; are you still connected to the internet?  Check our uptime at ()');
            /*
              this.errormodal_message = 'failure while logging out; are you still connected to the internet?  Check our uptime at';
              this.openModal(this.errorModal);
            */
        });
    }
};
NavComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
        selector: 'app-nav',
        template: __webpack_require__("../../../../../src/app/nav/nav.component.html"),
        styles: [__webpack_require__("../../../../../src/app/nav/nav.component.css")]
    }),
    __metadata("design:paramtypes", [typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_1__auth_service__["a" /* AuthService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__auth_service__["a" /* AuthService */]) === "function" && _a || Object, typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_2__appointment_service__["a" /* AppointmentService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__appointment_service__["a" /* AppointmentService */]) === "function" && _b || Object, typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_3__nav_service__["a" /* NavService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__nav_service__["a" /* NavService */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_4_ngx_cookie_service__["a" /* CookieService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4_ngx_cookie_service__["a" /* CookieService */]) === "function" && _d || Object])
], NavComponent);

var _a, _b, _c, _d;
//# sourceMappingURL=nav.component.js.map

/***/ }),

/***/ "../../../../../src/app/salesforce-only.directive.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* unused harmony export salesforceOnly */
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return SalesforceOnlyDirective; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_forms__ = __webpack_require__("../../../forms/@angular/forms.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};


function salesforceOnly() {
    return (control) => {
        const valid_email = control.value.toLowerCase().endsWith('salesforce.com');
        return !valid_email ? { 'salesforceOnly': { value: control.value } } : null;
    };
}
let SalesforceOnlyDirective = SalesforceOnlyDirective_1 = class SalesforceOnlyDirective {
    constructor() { }
    validate(control) {
        return (control.value !== null) ? salesforceOnly()(control) : null;
    }
};
SalesforceOnlyDirective = SalesforceOnlyDirective_1 = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["t" /* Directive */])({
        selector: '[appSalesforceOnly]',
        providers: [{ provide: __WEBPACK_IMPORTED_MODULE_1__angular_forms__["b" /* NG_VALIDATORS */], useExisting: SalesforceOnlyDirective_1, multi: true }]
    }),
    __metadata("design:paramtypes", [])
], SalesforceOnlyDirective);

var SalesforceOnlyDirective_1;
//# sourceMappingURL=salesforce-only.directive.js.map

/***/ }),

/***/ "../../../../../src/app/search/search.component.css":
/***/ (function(module, exports, __webpack_require__) {

exports = module.exports = __webpack_require__("../../../../css-loader/lib/css-base.js")(false);
// imports


// module
exports.push([module.i, "", ""]);

// exports


/*** EXPORTS FROM exports-loader ***/
module.exports = module.exports.toString();

/***/ }),

/***/ "../../../../../src/app/search/search.component.html":
/***/ (function(module, exports) {

module.exports = "<form id=\"searchForm\" (ngSubmit)=\"onSubmitSearch()\" #searchForm=\"ngForm\">\n  <div class=\"alert alert-danger\" role=\"alert\" *ngIf=\"appointmentService.searchResults != null && appointmentService.searchResults.message\">\n    <span class=\"glyphicon glyphicon-exclamation-sign\" aria-hidden=\"true\"></span>\n    <span class=\"sr-only\">Error:</span>\n    <span>\n        {{appointmentService.searchResults.message}}<br>\n    </span>\n  </div>\n\n  <div class=\"form-group\">\n    <label for=\"searchDate\">Date</label>\n    <input type=\"date\" class=\"form-control\" id=\"searchDate\" name=\"date\" ngModel>\n  </div>\n\n  <div class=\"form-group\">\n    <label for=\"searchLocation\">Location</label>\n      <select multiple=\"multiple\" id=\"searchLocation\" name=\"location\" class=\"form-control\"\n              [compareWith]=\"compareIdFn\" ngModel>\n      <option *ngFor=\"let locationOption of locationOptions\"\n              [ngValue]=\"locationOption\">{{locationOption.name}}</option>\n    </select>\n  </div>\n\n  <div class=\"advanced-controls\">\n    <div class=\"checkbox\">\n      <label>\n        <input name=\"bothsexes\" type=\"checkbox\" ngModel> ⚥\n      </label>\n      <label>\n        <input name=\"male\" type=\"checkbox\" ngModel> ♂\n      </label>\n      <label>\n        <input name=\"female\" type=\"checkbox\" ngModel> ♀\n      </label>\n    </div>\n  </div>\n\n  <button type=\"submit\" class=\"btn btn-default\">Submit</button>\n</form>\n\n<app-appointment-item *ngIf=\"searching\" [appointments]=\"appointments()\"\n                      [allowJoiningEvent]=true (joinEvent)=\"onAppointmentJoined($event)\">\n  No search results found!  Please retry your search.\n</app-appointment-item>\n"

/***/ }),

/***/ "../../../../../src/app/search/search.component.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
/* harmony export (binding) */ __webpack_require__.d(__webpack_exports__, "a", function() { return SearchComponent; });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__auth_service__ = __webpack_require__("../../../../../src/app/auth.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__appointment_service__ = __webpack_require__("../../../../../src/app/appointment.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__nav_service__ = __webpack_require__("../../../../../src/app/nav.service.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_4__angular_forms__ = __webpack_require__("../../../forms/@angular/forms.es5.js");
var __decorate = (this && this.__decorate) || function (decorators, target, key, desc) {
    var c = arguments.length, r = c < 3 ? target : desc === null ? desc = Object.getOwnPropertyDescriptor(target, key) : desc, d;
    if (typeof Reflect === "object" && typeof Reflect.decorate === "function") r = Reflect.decorate(decorators, target, key, desc);
    else for (var i = decorators.length - 1; i >= 0; i--) if (d = decorators[i]) r = (c < 3 ? d(r) : c > 3 ? d(target, key, r) : d(target, key)) || r;
    return c > 3 && r && Object.defineProperty(target, key, r), r;
};
var __metadata = (this && this.__metadata) || function (k, v) {
    if (typeof Reflect === "object" && typeof Reflect.metadata === "function") return Reflect.metadata(k, v);
};





let SearchComponent = class SearchComponent {
    constructor(authService, appointmentService, navService) {
        this.authService = authService;
        this.appointmentService = appointmentService;
        this.navService = navService;
        this.searching = false;
    }
    appointments() {
        // Returns a list of all possible appointments for search conditions provided.
        if (!this.appointmentService.searchResults) {
            return [];
        }
        return this.appointmentService.searchResults.youonly.concat(this.appointmentService.searchResults.everyone);
    }
    onAppointmentJoined() {
        this.navService.myevents();
        this.joinEvent.emit(true);
    }
    onSubmitSearch() {
        console.log('trigger search');
        this.searching = true;
        this.appointmentService.search(this.authService.token, this.searchForm).catch((err) => {
            console.log('Search Error!');
            console.log(err);
        });
    }
    compareIdFn(l1, l2) {
        return l1.id === l2.id;
    }
    ngOnInit() {
        setTimeout(() => {
            this.searchForm.form.controls.date.setValue(new Date().toISOString().split('T')[0]);
        }, 1500);
    }
};
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["E" /* Input */])(),
    __metadata("design:type", Array)
], SearchComponent.prototype, "foodOptions", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["E" /* Input */])(),
    __metadata("design:type", Array)
], SearchComponent.prototype, "locationOptions", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["R" /* Output */])(),
    __metadata("design:type", typeof (_a = typeof __WEBPACK_IMPORTED_MODULE_0__angular_core__["w" /* EventEmitter */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_0__angular_core__["w" /* EventEmitter */]) === "function" && _a || Object)
], SearchComponent.prototype, "joinEvent", void 0);
__decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_13" /* ViewChild */])('searchForm'),
    __metadata("design:type", typeof (_b = typeof __WEBPACK_IMPORTED_MODULE_4__angular_forms__["e" /* NgForm */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_4__angular_forms__["e" /* NgForm */]) === "function" && _b || Object)
], SearchComponent.prototype, "searchForm", void 0);
SearchComponent = __decorate([
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["n" /* Component */])({
        selector: 'app-search',
        template: __webpack_require__("../../../../../src/app/search/search.component.html"),
        styles: [__webpack_require__("../../../../../src/app/search/search.component.css")]
    }),
    __metadata("design:paramtypes", [typeof (_c = typeof __WEBPACK_IMPORTED_MODULE_1__auth_service__["a" /* AuthService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_1__auth_service__["a" /* AuthService */]) === "function" && _c || Object, typeof (_d = typeof __WEBPACK_IMPORTED_MODULE_2__appointment_service__["a" /* AppointmentService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_2__appointment_service__["a" /* AppointmentService */]) === "function" && _d || Object, typeof (_e = typeof __WEBPACK_IMPORTED_MODULE_3__nav_service__["a" /* NavService */] !== "undefined" && __WEBPACK_IMPORTED_MODULE_3__nav_service__["a" /* NavService */]) === "function" && _e || Object])
], SearchComponent);

var _a, _b, _c, _d, _e;
//# sourceMappingURL=search.component.js.map

/***/ }),

/***/ "../../../../../src/environments/environment.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
// The file contents for the current environment will overwrite these during build.
// The build system defaults to the dev environment which uses `environment.ts`, but if you do
// `ng build --env=prod` then `environment.prod.ts` will be used instead.
// The list of which env maps to which file can be found in `.angular-cli.json`.
const environment = {
    production: false
};
/* harmony export (immutable) */ __webpack_exports__["a"] = environment;

//# sourceMappingURL=environment.js.map

/***/ }),

/***/ "../../../../../src/main.ts":
/***/ (function(module, __webpack_exports__, __webpack_require__) {

"use strict";
Object.defineProperty(__webpack_exports__, "__esModule", { value: true });
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_0__angular_core__ = __webpack_require__("../../../core/@angular/core.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_1__angular_platform_browser_dynamic__ = __webpack_require__("../../../platform-browser-dynamic/@angular/platform-browser-dynamic.es5.js");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_2__app_app_module__ = __webpack_require__("../../../../../src/app/app.module.ts");
/* harmony import */ var __WEBPACK_IMPORTED_MODULE_3__environments_environment__ = __webpack_require__("../../../../../src/environments/environment.ts");




if (__WEBPACK_IMPORTED_MODULE_3__environments_environment__["a" /* environment */].production) {
    Object(__WEBPACK_IMPORTED_MODULE_0__angular_core__["_20" /* enableProdMode */])();
}
Object(__WEBPACK_IMPORTED_MODULE_1__angular_platform_browser_dynamic__["a" /* platformBrowserDynamic */])().bootstrapModule(__WEBPACK_IMPORTED_MODULE_2__app_app_module__["a" /* AppModule */])
    .catch(err => console.log(err));
//# sourceMappingURL=main.js.map

/***/ }),

/***/ 0:
/***/ (function(module, exports, __webpack_require__) {

module.exports = __webpack_require__("../../../../../src/main.ts");


/***/ })

},[0]);
//# sourceMappingURL=main.bundle.js.map