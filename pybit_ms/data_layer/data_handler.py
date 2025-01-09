import os
import csv
import pandas as pd
from typing import List, Dict, Any
from IPython.display import display_html

class DataHandler:
    """
    A class responsible for storing, formatting, and visualizing data retrieved
    from the customized Bybit API modules.
    """

    def __init__(self, base_dir: str = "data/"):
        """
        Initialize the data handler.
        
        Args:
            base_dir (str): Directory where CSV files or other outputs will be saved.
        """
        self.base_dir = base_dir
        os.makedirs(self.base_dir, exist_ok=True)


    def store_to_csv(self, data: List[Dict[str, Any]], filename: str) -> str:
        """
        Store data (list of dictionaries) into a CSV file.
        
        Args:
            data (list[dict]): A list of dictionaries representing rows of data.
            filename (str): The CSV filename (without path).
        
        Returns:
            str: Full path of the created CSV file.
        """
        if not data:
            raise ValueError("No data provided to store.")
        
        filepath = os.path.join(self.base_dir, filename)
        
        # Extract headers from the first element's keys
        headers = list(data[0].keys())
        
        with open(filepath, mode='w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=headers)
            writer.writeheader()
            writer.writerows(data)
        
        return filepath


    def load_from_csv(self, filename: str) -> List[Dict[str, Any]]:
        """
        Load data from a CSV file into a list of dictionaries.
        
        Args:
            filename (str): The CSV filename (without path).
        
        Returns:
            list[dict]: A list of data rows as dictionaries.
        """
        filepath = os.path.join(self.base_dir, filename)
        
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        with open(filepath, mode='r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader)
        

    def is_not_zero(self, value):
        """Check if a value is numeric and not zero."""
        try:
            num = float(value)
            return num != 0
        except ValueError:
            return False


    def format_with_spaces(self, value):
        """
        Format numeric values to have commas replaced by spaces, 
        e.g., 1,234,567.8 -> 1 234 567.8 Only applies if `value` is numeric.
        """
        try:
            num = float(value)
            if num.is_integer():
                num = int(num)

            if num > 999999:
                formatted = f"{num:,}".replace(",", " ")
            else:
                formatted = str(num)
        except ValueError:
            formatted = value
        return formatted
    
    def format_empty(self, resp:dict, key:str):
        if not self.is_not_zero(resp.get(key, 0)):
            resp[key] = '-'


    def format_time(self, resp:dict, key:str, form:str):
        """
        Convert timestamp to human-readable
        """
        if key in resp:
            try:
                resp[key] = pd.to_datetime(
                    int(resp.get(key, '')), unit='ms'
                ).strftime(form)
            except (ValueError, TypeError):
                resp[key] = '-'
    

    def format_take_profit(self, resp:dict):
        """
        Take-profit logic
        """
        tp_price = resp.get('takeProfit', 0)
        tp_limit = resp.get('tpLimitPrice', 0)
        if self.is_not_zero(tp_price) or self.is_not_zero(tp_limit):
            resp['takeProfit'] = (
                f"{'limit' if self.is_not_zero(tp_limit) else 'market'}:  \
                {self.format_with_spaces(tp_price) if self.is_not_zero(tp_price) \
                else self.format_with_spaces(tp_limit)}"
            )
        else:
            resp['takeProfit'] = '-'
        resp.pop('tpLimitPrice', None)


    def format_stop_loss(self, resp:dict):
        """
        Stop-loss logic
        """
        sl_price = resp.get('stopLoss', 0)
        sl_limit = resp.get('slLimitPrice', 0)
        if self.is_not_zero(sl_price) or self.is_not_zero(sl_limit):
            resp['stopLoss'] = (
                f"{'limit' if self.is_not_zero(sl_limit) else 'market'}:  \
                {self.format_with_spaces(sl_price) if self.is_not_zero(sl_price) \
                else self.format_with_spaces(sl_limit)}"
            )
        else:
            resp['stopLoss'] = '-'
        resp.pop('slLimitPrice', None)

    
    def format_trigger_price(self, resp:dict):
        """
        Trigger price logic
        """
        trig_price = resp.get('triggerPrice', 0)
        trig_formatted = self.format_with_spaces(trig_price)
        arrow = '↑' if resp.get('triggerDirection', '') == '1' else '↓'
        trig_by = resp.get('triggerBy', '')
        status = resp.get('orderStatus', '')
        if self.is_not_zero(trig_price):
            resp['triggerPrice'] = f"{arrow} {status} ({trig_by}): {trig_formatted}"
        else:
            resp['triggerPrice'] = '-'
        
        resp.pop('triggerDirection', None)
        resp.pop('orderStatus', None)
        resp.pop('triggerBy', None)


    def format_id(self, resp:dict):
        """
        Order Id logic
        """
        order_link = resp.get('orderLinkId', '')
        order_id = resp.get('orderId', '')
        if 'orderLinkId' in resp:
            resp['orderLinkId'] = f"link: {order_link}"
        if 'orderId' in resp:
            resp['orderId'] = f"id: {order_id}"
    

    def format_leverage(self, resp:dict):
        """
        Leverage logic
        """
        leverage = resp.get('leverage', '')
        trade_mode = 'isolated' if resp.get('tradeMode', 0) else 'cross'
        if 'tradeMode' in resp and 'leverage' in resp:
            resp['leverage'] = f"{trade_mode}: {leverage}X"
        resp.pop('tradeMode', None)


    def format_fees(self, resp:dict):
        """
        Execution fees logic
        """
        exec_fee = resp.get('execFee', '')
        fee_currency = resp.get('feeCurrency', '')
        if 'execFee' in resp and 'feeCurrency' in resp:
            try:
                exec_fee_val = float(exec_fee)
                resp['execFee'] = f"{exec_fee_val:.4f} {fee_currency}"
            except (ValueError, TypeError):
                resp['execFee'] = f"0.0000 {fee_currency}"
        resp.pop('feeCurrency', None)

    
    def format_order_type(self, resp:dict, key1:str, key3:str = None):
        """
        Order type logic
            - key1 = 'execType' or 'orderStatus'
            - key3 = 'timeInForce'. Default=None
        """
        order_type = resp.get('orderType', '')
        exec_type = resp.get(key1, '')
        time_in_force = resp.get(key3, '')
        if key1 in resp and 'orderType' in resp:
            if key3 in resp:
                resp['orderType'] = f"{exec_type} ({order_type}, {time_in_force})"
            else:
                resp['orderType'] = f"{exec_type} ({order_type})"

        if time_in_force == '':
            resp.pop(key1, None)
        resp.pop(key3, None)


    def format_dashboard(self, df):
        """
        Apply custom styling to a pandas DataFrame for display in a Jupyter environment.
        All cells have a black background with consistent table and text formatting.
        
        Args:
            df (pd.DataFrame): The dataframe to style.
        
        Returns:
            pd.io.formats.style.Styler: Styled dataframe for display.
        """
        header_styles = [
            {
                'selector': 'caption',
                'props': [
                    ('color', 'white'),
                    ('font-size', '16px'),
                    ('font-weight', 'bold'),
                    ('text-align', 'center'),
                    ('caption-side', 'top')
                ]
            }
        ]

        styled = (
            df.style
            .map(lambda _: 'background-color: black')  # Black background for all cells
            .set_properties(**{'text-align': 'right'})  # Right-align text
            .set_table_attributes('style="font-size: 12px; border: 2px solid black;"')  # Table border and font size
            .format(self.format_with_spaces)  # Custom cell formatting
            .set_table_styles(header_styles)  # Apply header styles
        )
        return styled


    def format_and_display(self, df:pd.DataFrame, caption:str):
        styled_df = self.format_dashboard(df).set_caption(caption)
        html = styled_df._repr_html_()
        display_html(html, raw=True)


    def save_dataframe_to_csv(self, df: pd.DataFrame, filename: str) -> str:
        """
        Convert a DataFrame into a CSV file for further analysis or archiving.
        
        Args:
            df (pd.DataFrame): DataFrame containing the data.
            filename (str): The CSV filename (without path).

        Returns:
            str: Full path of the created CSV file.
        """
        df = self.format_dataframe(df)
        filepath = os.path.join(self.base_dir, filename)
        df.to_csv(filepath, index=False)
        return filepath
