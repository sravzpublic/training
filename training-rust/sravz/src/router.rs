use std::{error::Error, collections::HashMap};
use crate::{models::Message, leveraged_funds::LeveragedFunds};

#[derive(Debug)]
enum MessageID {
    LeverageFundsNasdaq100 = 1,
    LeverageFundsAll = 2,
}

pub struct Router {
    leveraged_funds: LeveragedFunds
}

impl Router {

    pub fn new() -> Self {
        // TODO: Check proper dependency injection
        let leveraged_funds = LeveragedFunds::new();
        Router { leveraged_funds }
    }

    // pub async fn setup_routes(&self) {
    //     self.functions.insert(OrderedFloat(1.0),  &self.leveraged_funds.leverage_funds_nasdaq100);
    //     self.functions.insert(OrderedFloat(2.0),  &self.leveraged_funds.leverage_funds_nasdaq100);
    //     // match message_id {
    //     //     MessageID::LeverageFundsNasdaq100 => self.leveraged_funds.leverage_funds_nasdaq100(message).await,
    //     //     MessageID::LeverageFundsAll => self.leveraged_funds.leverage_funds_nasdaq100(message).await,
    //     // }
    // }

    pub async fn process_message(&self, mut message: Message) -> Result<Message, Box<dyn Error>>  {
        match message.fun_n.as_str() {
            "leverage_funds_nasdaq100" => self.leveraged_funds.leverage_funds_nasdaq100(message).await,
            // 2.0..=2.9 => self.leveraged_funds.leverage_funds_nasdaq100(message).await,
            _ => {
                message.exception_message = "Message ID not implemented".to_owned();
                Err(Box::new(message))
            }
        }
    }
}
