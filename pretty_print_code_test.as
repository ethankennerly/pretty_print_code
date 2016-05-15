package
{
    /**
     * After running pretty_print_code.py on this file
     * Expect no change to the format.
     */
    public class pretty_print_code_test
    {
        /**
         * Comment
         */
        public function f(){
            var d = {a: 1};
            d["a"] = 2;
            if (d["a"] == 1) {
                trace("1");
            }
            else {
                trace("Not 1");
            }
            d = {a: {b: {
                        c: 0}}};
        }
    }
}