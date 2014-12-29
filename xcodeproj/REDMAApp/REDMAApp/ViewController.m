//
//  ViewController.m
//  REDMAApp
//
//  Created by Sajeev Kohli on 2014-12-26.
//  Copyright (c) 2014 Saj. All rights reserved.
//

#import "ViewController.h"

@interface ViewController ()
{
    NSString *waterValue;
    NSString *smokeValue;
    bool waterButtonToggle;
    bool smokeButtonToggle;
    bool waterOK;
    bool smokeOK;
}

@end

@implementation ViewController

/**
 * This method is called when the view controller is loaded.
 */
- (void)viewDidLoad {
    [super viewDidLoad];
    // connect to the web service and get data when the
    // view controller is loaded for the first time.
    [self getDataFromWebservice];
    
    // create a thread to automatically refresh data every 10 seconds
    NSThread* refreshThread = [[NSThread alloc] initWithTarget:self
                            selector:@selector(refreshData)
                            object:nil];
    [refreshThread start];  // Actually create the thread
    
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
}

- (void) refreshData {
    for(;;) {
        [NSThread sleepForTimeInterval:10.0f];
        [self getDataFromWebservice];
    }
}

/**
 * This method is called when the refresh button is clicked.
 */
- (IBAction)handleRefreshButtonClick:(id)sender {
    // get data from the web service when the refresh button
    // is clicked.
    [self getDataFromWebservice];
}


/**
 * This method is called when the smoke data button is clicked.
 */
- (IBAction)handleSmokeButtonClick:(id)sender {
    // smokeButtonToggle is used to toggle the state of the smoke button.
    if(smokeButtonToggle) {
        // if the toggle value is YES, display the numeric value retrieved
        // from the web service, then set the toggle value to NO
        [self.smokeButton setTitle:smokeValue forState:UIControlStateNormal];
        smokeButtonToggle = NO;
    } else {
        // if the toggle value is NO, display OK or Alert
        // then set the toggle value to YES
        if(smokeOK) {
            // display OK if the numeric value retrieved for smoke from the
            // web service is within normal limits (i.e. not exceeding threshold)
            [self.smokeButton setTitle:@"OK" forState:UIControlStateNormal];
        } else {
            // display Alert if the numeric value retrieved for smoke from the
            // web service is not within normal limits (i.e. not exceeding threshold)
            [self.smokeButton setTitle:@"Alert" forState:UIControlStateNormal];
        }
        smokeButtonToggle = YES;
    }
}

/**
 * This method is called when the water data button is clicked.
 */
- (IBAction)handleWaterButtonClick:(id)sender {
    // waterButtonToggle is used to toggle the state of the water button.
    if(waterButtonToggle) {
        // if the toggle value is YES, display the numeric value retrieved
        // from the web service, then set the toggle value to NO
        [self.waterButton setTitle:waterValue forState:UIControlStateNormal];
        waterButtonToggle = NO;
    } else {
        // if the toggle value is NO, display OK or Alert
        // then set the toggle value to YES
        if(waterOK) {
            // display OK if the numeric value retrieved for water from the
            // web service is within normal limits (i.e. not exceeding threshold)
            [self.waterButton setTitle:@"OK" forState:UIControlStateNormal];
        } else {
            // display Alert if the numeric value retrieved for water from the
            // web service is not within normal limits (i.e. not exceeding threshold)
            [self.waterButton setTitle:@"Alert" forState:UIControlStateNormal];
        }
        waterButtonToggle = YES;
    }
}

/**
 * This method is called to reset all data and text to defaults.
 */
- (void) clearData{
    waterValue = @"";
    smokeValue = @"";
    waterButtonToggle = YES;
    smokeButtonToggle = YES;
    waterOK = YES;
    smokeOK = YES;
    self.errorLabel.text = @"";
    self.temperatureLabel.text = @"";
    [self.waterButton setTitle:@"" forState:UIControlStateNormal];
    [self.smokeButton setTitle:@"" forState:UIControlStateNormal];
    self.timestampLabel.text = @"";
}

/**
 * This method is called to display an error message on the app.
 */
- (void) displayError {
    [self clearData];
    self.errorLabel.text = @"WebService connection failed :-(";
    self.errorLabel.textColor = [UIColor redColor];
}


/**
 * Motherload. This method does the important work here.
 * It talks to the web service to retrieve sensor data stored
 * in the database.
 */
-(void) getDataFromWebservice {
    bool errorOccurred = NO;
    @try {
        // reset data before doing anything else
        [self clearData];
        
        // connect to the web service by
        // 1. creating a URL object
        // 2. creating a request object
        // 3. creating a URL Connection object
        // 4. sending an asynchronous request to the web service URL
        NSURL *subscriberURL = [NSURL URLWithString: @"http://jkhomeserver.dyndns.org:3000/sensoryData/1"];
        NSURLRequest *subscriberRequest = [NSURLRequest requestWithURL:subscriberURL];
        [NSURLConnection sendAsynchronousRequest:subscriberRequest
                                    queue:[NSOperationQueue mainQueue]
                               completionHandler:^(NSURLResponse *response,
                                                   NSData *data, NSError *connectionError)
         {
             // Ensure that data was returned and that there were no connection errors
             // before proceeding
             if(data.length > 0 && connectionError == nil) {
                 // Read the required data from the returned JSON response
                 NSError *myError = nil;
                 NSDictionary *subscriberResDict = [NSJSONSerialization
                                                    JSONObjectWithData:data
                                                    options:0
                                                    error:&myError];
                 // the data that we care about is in the json tag
                 NSArray *subscriberJSONRes = [subscriberResDict objectForKey:@"json"];
                 for (id tempElem in subscriberJSONRes) {
                     if( ![tempElem isKindOfClass:[NSDictionary class]]) {
                         // this should never happen
                         NSLog(@"The value %@ in the array is not a dictionary", [tempElem stringValue]);
                         continue;
                     }
                     // the json tag should return a list of key-value pairs i.e. a dictionary
                     NSDictionary *elem = (NSDictionary*)tempElem;
                     for(id key in elem) {
                         // iterate over the dictionary to get key value pairs
                         id value = [elem objectForKey:key];
                         // obtain the key data as a string
                         NSString *keyAsString = nil;
                         if([key isKindOfClass:[NSString class]]) {
                            keyAsString = (NSString *)key;
                         } else {
                             keyAsString = [key stringValue];
                         }
                         // obtain the value data as a string
                         NSString *valueAsString = nil;
                         if([value isKindOfClass:[NSString class]]) {
                             valueAsString = (NSString *)value;
                         } else if ([value isKindOfClass:[NSNumber class]]) {
                             // if the value data is a number, format it to 2 decimal places
                             NSNumberFormatter *numberFormatter = [[NSNumberFormatter alloc] init];
                             [numberFormatter setNumberStyle:NSNumberFormatterDecimalStyle];
                             [numberFormatter setUsesGroupingSeparator:NO];
                             [numberFormatter setMaximumFractionDigits:2];
                             [numberFormatter setMinimumFractionDigits:0];
                             valueAsString = [numberFormatter stringFromNumber:(NSNumber*)value];
                         } else {
                             valueAsString = [value stringValue];
                         }
                         
                         if([keyAsString isEqualToString:@"sensor1" ] ) {
                             // this is the actual temperature data
                             self.temperatureLabel.text = valueAsString;
                         } else if([keyAsString isEqualToString:@"sensor1th" ]) {
                             // this determines if the temperature is above or below threshold
                             if ([value isKindOfClass:[NSNumber class]]) {
                                 float tempVal = [(NSNumber*)value floatValue];
                                 if(tempVal > 0.0) {
                                     // we have an issue
                                     self.temperatureLabel.textColor = [UIColor redColor];
                                 } else {
                                     // all is good
                                     self.temperatureLabel.textColor = [UIColor greenColor];
                                 }
                             } else {
                                 // this should never happen
                                 NSLog(@"sensorth1 is not a float value");
                             }
                         } else if( [keyAsString isEqualToString:@"sensor2"]) {
                             // this is the acutal water data
                             waterValue = valueAsString;
                         } else if([keyAsString isEqualToString:@"sensorth2" ]) {
                             // this determines if the water value is above or below threshold
                             if ([value isKindOfClass:[NSNumber class]]) {
                                 float tempVal = [(NSNumber*)value floatValue];
                                 if(tempVal > 0.0) {
                                     // we have an issue
                                     [self.waterButton setTitle:@"Alert" forState:UIControlStateNormal];
                                     [self.waterButton setTitleColor:[UIColor redColor] forState:UIControlStateNormal];
                                     waterOK = NO;
                                 } else {
                                     // all is good
                                     [self.waterButton setTitle:@"OK" forState:UIControlStateNormal];
                                     [self.waterButton setTitleColor:[UIColor greenColor] forState:UIControlStateNormal];
                                     waterOK = YES;
                                 }
                             } else {
                                 // this should never happen
                                 NSLog(@"sensorth2 is not a float value");
                             }
                         } else if( [keyAsString isEqualToString:@"sensor3"]) {
                             // this is the actual smoke data
                             smokeValue = valueAsString;
                         } else if([keyAsString isEqualToString:@"sensorth3" ]) {
                             // this determines if the smoke value is above or below threshold
                             if ([value isKindOfClass:[NSNumber class]]) {
                                 float tempVal = [(NSNumber*)value floatValue];
                                 if(tempVal > 0.0) {
                                     // we have an issue
                                     [self.smokeButton setTitle:@"Alert" forState:UIControlStateNormal];
                                     [self.smokeButton setTitleColor:[UIColor redColor] forState:UIControlStateNormal];
                                     smokeOK = NO;
                                 } else {
                                     // all is good
                                     [self.smokeButton setTitle:@"OK" forState:UIControlStateNormal];
                                     [self.smokeButton setTitleColor:[UIColor greenColor] forState:UIControlStateNormal];
                                     smokeOK = YES;
                                 }
                             } else {
                                 // this should never happen
                                 NSLog(@"sensorth2 is not a float value");
                             }
                         } else if( [keyAsString isEqualToString:@"timestamp"]) {
                             /// this is the timestamp data i.e. the time when the data was retrieved
                             self.timestampLabel.text = valueAsString;
                         }
                     }
                 }
             } else {
                 // this means that either an error occurred or no data was retrieved
                 // from the web service - either case this is BAD
                 [self displayError];
             }
         }];

    }
    @catch (NSException *exception) {
        NSLog(exception.description);
        errorOccurred = YES;
    }
    @finally {
        if(errorOccurred == YES) {
            [self displayError];
        }
    }
}

@end
