# -*- coding: utf-8 -*-

# Baqir Khan
# Software Engineer (Backend)
from datetime import datetime
import asyncio


# Convert time from string format to python's datetime object for easy comparisons
def isodate_to_datetime_obj(isodate):
    if type(isodate) == bytes:
        return datetime.strptime(isodate.decode('utf-8'), "%Y-%m-%dT%H:%M:%S.%fZ")
    elif type(isodate) == str:
        return datetime.strptime(isodate, "%Y-%m-%dT%H:%M:%S.%fZ")


class LogReader:
    # Variables used in API Output JSON
    START_DATE = "start_date"
    END_DATE = "end_date"
    LOGS = "logs"
    TIME = "time"
    MESSAGE = "message"
    LOGS_COUNT = "logs_count"

    def __init__(self, start_date, end_date, mapping, number_of_lines, filename):
        self.start_date = start_date
        self.end_date = end_date
        self.mapping = mapping
        self.number_of_lines = number_of_lines
        self.filename = filename

        # Initialize results dictionary that will be used to send results back
        self.results = {self.START_DATE: start_date, self.END_DATE: end_date, self.LOGS_COUNT: 0, self.LOGS: []}

    # Given offset('value' field in 'mapping' dictionary), return file pointer to that location
    def __get_file_pointer_at_offset(self, offset):
        fp = open(self.filename, 'rb')
        fp.seek(offset, 1)
        return fp

    # Parses date from line by splitting on space (' ') and taking the first element
    def __get_date_at_file_pointer(self, file_pointer):
        return file_pointer.readline().split()[0]

    # Binary search in O(log(n)) and returns the line number right before start_date
    def __binary_search(self, target_date):
        lo, hi = 1, self.number_of_lines
        while lo <= hi:
            mid = (lo + hi) >> 1
            fp_at_mid = self.__get_file_pointer_at_offset(self.mapping[mid])
            date_at_mid_isoformat = self.__get_date_at_file_pointer(fp_at_mid)
            date_at_mid_datetime = isodate_to_datetime_obj(date_at_mid_isoformat)
            if date_at_mid_datetime == target_date:
                return mid
            elif date_at_mid_datetime < target_date:
                lo = mid + 1
            else:
                hi = mid - 1
        return lo

    # Loops from line given by binary search until end date is reached
    # def __populate_error_logs(self, offset):
    async def __populate_error_logs(self, offset):
        fp = self.__get_file_pointer_at_offset(offset)
        end_date_isoformat = isodate_to_datetime_obj(self.end_date)
        start_date_isoformat = isodate_to_datetime_obj(self.start_date)
        count = 0
        for i, line in enumerate(fp):
            line = line.decode('utf-8')
            line_splitted = line.split()
            line_date = isodate_to_datetime_obj(line_splitted[0])

            # Current log date not in range as required by client, break
            if line_date > end_date_isoformat or line_date < start_date_isoformat:
                break

            count += 1
            self.results[self.LOGS].append({self.TIME: line_splitted[0], self.MESSAGE: " ".join(line_splitted[1:])})
        self.results[self.LOGS_COUNT] = count

    # The only public function which can be accessed outside the class, entry point.
    def build(self):
        line_start = self.__binary_search(isodate_to_datetime_obj(self.start_date))

        # USING Async/Await
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(self.__populate_error_logs(self.mapping[line_start]))

        # Without using Async await
        # self.__populate_error_logs(self.mapping[line_start])
        return self.results
